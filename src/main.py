"""Membrain MCP server entry point.

Wires a single shared MembrainClient into the FastMCP lifespan and registers every
tool module under src/tools/. This file contains no Membrain business logic: it is
purely composition/wiring.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import PackageNotFoundError, version

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import Settings
from src.context import AppContext
from src.membrain_client import MembrainClient
from src.tools import activities, companies, contacts, opportunities, prospects, reference

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("membrain_mcp")


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Create the shared MembrainClient for the server's lifetime and close it on shutdown."""
    settings = Settings()  # membrain_api_key is read from the environment / .env
    client = MembrainClient(
        base_url=settings.membrain_base_url,
        api_key=settings.membrain_api_key.get_secret_value(),
        timeout_seconds=settings.membrain_timeout_seconds,
        max_retries=settings.membrain_max_retries,
    )
    logger.info("membrain client started", extra={"base_url": settings.membrain_base_url})
    try:
        yield AppContext(client=client)
    finally:
        await client.aclose()
        logger.info("membrain client closed")


mcp: FastMCP = FastMCP("membrain", lifespan=lifespan)

companies.register(mcp)
contacts.register(mcp)
opportunities.register(mcp)
prospects.register(mcp)
activities.register(mcp)
reference.register(mcp)


@mcp.custom_route("/api/v1/internal/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Liveness endpoint for container orchestration (e.g. Kubernetes probes).

    Deliberately does NOT call Membrain: Membrain is a third-party SaaS outside our
    control, and if this same endpoint is wired as both the liveness and readiness
    probe, a Membrain outage would otherwise cause Kubernetes to restart this pod in a
    loop for a dependency it can do nothing about. `dependencies` is therefore always
    empty; only served when running under the "http" transport (see
    .docker/Dockerfile), unused for local stdio use.
    """
    try:
        app_version = version("membrain-mcp")
    except PackageNotFoundError:
        app_version = "unknown"
    return JSONResponse({"status": "OK", "version": app_version, "dependencies": {}})


def main() -> None:
    """Entry point for the `membrain-mcp` console script (see pyproject.toml).

    Transport defaults to stdio (local use, spawned by Claude Desktop/Code). Set
    MCP_TRANSPORT=http (plus MCP_HOST/MCP_PORT) for a containerized/remote deployment.
    """
    settings = Settings()  # membrain_api_key is read from the environment / .env
    if settings.mcp_transport == "http":
        logger.info(
            "starting membrain mcp server over http",
            extra={"host": settings.mcp_host, "port": settings.mcp_port},
        )
        mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
