"""MCP tools for the Membrain Prospect object. Read-only in V1 (see project plan).

Each tool is a thin wrapper around a plain async function that takes a
`MembrainClient` directly, keeping the logic unit-testable without depending on
FastMCP's decorator/Context internals.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Context, FastMCP

from src.membrain_client import MembrainClient
from src.models.prospect import Prospect, ProspectSearchParams
from src.tools._shared import dump, dump_params, get_client, paged_dump


async def _search_prospects(params: ProspectSearchParams, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get("prospects/", params=dump_params(params))
    return paged_dump(raw, Prospect)


async def _get_prospect(prospect_id: str, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get(f"prospects/{prospect_id}")
    return dump(Prospect.model_validate(raw))


def register(mcp: FastMCP) -> None:
    """Register all Prospect tools on the given FastMCP server instance."""

    @mcp.tool()
    async def search_prospects(params: ProspectSearchParams, ctx: Context) -> dict[str, Any]:
        """Search Prospects in Membrain (GET /prospects/).

        Returns a paged result: {count, from, to, items}. Page further by calling again
        with `from_index` set to the previous `to`.
        """
        return await _search_prospects(params, get_client(ctx))

    @mcp.tool()
    async def get_prospect(prospect_id: str, ctx: Context) -> dict[str, Any]:
        """Read a single Prospect by its GUID (GET /prospects/{Id})."""
        return await _get_prospect(prospect_id, get_client(ctx))
