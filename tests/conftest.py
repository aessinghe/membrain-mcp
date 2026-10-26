"""Shared pytest fixtures for the Membrain MCP server test suite.

No test in this suite ever calls the real Membrain API: all HTTP traffic is
intercepted by respx.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest

from src.membrain_client import MembrainClient

BASE_URL = "https://fake.membrain.test/API/v2/"
API_KEY = "test-api-key"


async def _instant_backoff(_attempt: int) -> None:
    """Replace the real exponential backoff sleep so retry tests run instantly."""
    return None


@pytest.fixture
async def client(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[MembrainClient]:
    """A MembrainClient pointed at a fake base URL, with retry backoff sleeps disabled."""
    monkeypatch.setattr(MembrainClient, "_sleep_backoff", staticmethod(_instant_backoff))
    c = MembrainClient(base_url=BASE_URL, api_key=API_KEY, timeout_seconds=5, max_retries=2)
    try:
        yield c
    finally:
        await c.aclose()
