"""Async HTTP client for the Membrain REST API v2.

This module is the only place in the codebase that talks to Membrain over the network.
It knows nothing about MCP or business semantics: it just sends authenticated HTTP
requests, retries transient failures on idempotent methods, and raises a typed error
on non-2xx responses.
"""

from __future__ import annotations

import asyncio
import logging
import random
from types import TracebackType
from typing import Any, Literal, Self

import httpx

logger = logging.getLogger("membrain_mcp.client")

# Status codes considered transient and worth retrying on idempotent requests.
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# Membrain documents ?APIKey=xxx as well as a request header named APIKey; the header
# form is used here so the key never ends up in URLs (query strings tend to leak into
# access logs, proxies, and browser history).
_API_KEY_HEADER = "APIKey"


class MembrainAPIError(Exception):
    """Raised when Membrain returns a non-2xx response.

    The Membrain documentation does not specify an error response schema, so the raw
    body is preserved as-is rather than parsed into an assumed structure.
    """

    def __init__(self, status_code: int, method: str, url: str, body: str) -> None:
        self.status_code = status_code
        self.method = method
        self.url = url
        self.body = body
        super().__init__(f"Membrain API error {status_code} on {method} {url}: {body[:500]}")


class MembrainClient:
    """Thin async wrapper around httpx for the Membrain REST API.

    Use as an async context manager so the underlying connection pool is closed
    cleanly:

        async with MembrainClient(base_url, api_key) as client:
            data = await client.get("/companies/", params={"Name": "Acme*"})
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout_seconds: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={_API_KEY_HEADER: api_key},
            timeout=timeout_seconds,
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.aclose()

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """Perform a GET request. Retried on transient errors (idempotent)."""
        return await self._request("GET", path, params=params, idempotent=True)

    async def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        """Perform a POST request. Never retried: retrying a create could duplicate data."""
        return await self._request("POST", path, json=json, idempotent=False)

    async def put(self, path: str, json: dict[str, Any] | None = None) -> Any:
        """Perform a PUT request. Retried on transient errors (updates are idempotent)."""
        return await self._request("PUT", path, json=json, idempotent=True)

    async def _request(
        self,
        method: Literal["GET", "POST", "PUT"],
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        idempotent: bool,
    ) -> Any:
        # Drop None values so optional filters are omitted from the query string
        # instead of being sent as the literal string "None".
        clean_params = (
            {k: v for k, v in params.items() if v is not None} if params is not None else None
        )
        clean_json = (
            {k: v for k, v in json.items() if v is not None} if json is not None else None
        )

        attempt = 0
        while True:
            attempt += 1
            try:
                response = await self._client.request(
                    method, path, params=clean_params, json=clean_json
                )
            except httpx.TransportError:
                if idempotent and attempt <= self._max_retries:
                    await self._sleep_backoff(attempt)
                    logger.warning(
                        "membrain request transport error, retrying",
                        extra={"method": method, "path": path, "attempt": attempt},
                    )
                    continue
                raise

            logger.info(
                "membrain request completed",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "attempt": attempt,
                },
            )

            if response.status_code in _RETRYABLE_STATUS_CODES and (
                idempotent and attempt <= self._max_retries
            ):
                await self._sleep_backoff(attempt)
                continue

            if response.status_code >= 300:
                raise MembrainAPIError(
                    status_code=response.status_code,
                    method=method,
                    url=str(response.request.url),
                    body=response.text,
                )

            if not response.content:
                return None
            return response.json()

    @staticmethod
    async def _sleep_backoff(attempt: int) -> None:
        base_delay = 0.5 * (2 ** (attempt - 1))
        # Jitter for retry backoff timing only, not a cryptographic use of randomness.
        jitter = random.uniform(0, 0.25)  # nosec B311
        await asyncio.sleep(base_delay + jitter)
