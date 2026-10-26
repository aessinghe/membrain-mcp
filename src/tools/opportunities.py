"""MCP tools for the Membrain Opportunity (Sales Project) object
(GET/POST/PUT /opportunities/).

Each tool is a thin wrapper around a plain async function that takes a
`MembrainClient` directly, keeping the logic unit-testable without depending on
FastMCP's decorator/Context internals.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Context, FastMCP

from src.membrain_client import MembrainClient
from src.models.common import merge_custom_fields
from src.models.opportunity import (
    Opportunity,
    OpportunityCreate,
    OpportunitySearchParams,
    OpportunityUpdate,
)
from src.tools._shared import dump, dump_params, get_client, paged_dump


async def _search_opportunities(
    params: OpportunitySearchParams, client: MembrainClient
) -> dict[str, Any]:
    raw = await client.get("opportunities/", params=dump_params(params))
    return paged_dump(raw, Opportunity)


async def _get_opportunity(opportunity_id: str, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get(f"opportunities/{opportunity_id}")
    return dump(Opportunity.model_validate(raw))


async def _create_opportunity(
    params: OpportunityCreate, client: MembrainClient
) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.post("opportunities/", json=payload)
    return dump(Opportunity.model_validate(raw))


async def _update_opportunity(
    opportunity_id: str, params: OpportunityUpdate, client: MembrainClient
) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.put(f"opportunities/{opportunity_id}", json=payload)
    return dump(Opportunity.model_validate(raw))


def register(mcp: FastMCP) -> None:
    """Register all Opportunity tools on the given FastMCP server instance."""

    @mcp.tool()
    async def search_opportunities(
        params: OpportunitySearchParams, ctx: Context
    ) -> dict[str, Any]:
        """Search Opportunities (Sales Projects) in Membrain (GET /opportunities/).

        Returns a paged result: {count, from, to, items}. Page further by calling again
        with `from_index` set to the previous `to`.
        """
        return await _search_opportunities(params, get_client(ctx))

    @mcp.tool()
    async def get_opportunity(opportunity_id: str, ctx: Context) -> dict[str, Any]:
        """Read a single Opportunity (Sales Project) by its GUID (GET /opportunities/{Id})."""
        return await _get_opportunity(opportunity_id, get_client(ctx))

    @mcp.tool()
    async def create_opportunity(params: OpportunityCreate, ctx: Context) -> dict[str, Any]:
        """Create a new Opportunity (Sales Project) in Membrain (POST /opportunities/).

        Requires Name, CompanyId, ProcessId and OpportunityOwnerId. Use `list_processes`
        (process_type="sales") to discover ProcessId and `list_users` for OpportunityOwnerId.
        """
        return await _create_opportunity(params, get_client(ctx))

    @mcp.tool()
    async def update_opportunity(
        opportunity_id: str, params: OpportunityUpdate, ctx: Context
    ) -> dict[str, Any]:
        """Update an existing Opportunity (Sales Project) in Membrain (PUT /opportunities/{Id}).

        Only the fields provided in `params` are sent; omitted fields are left unchanged.
        """
        return await _update_opportunity(opportunity_id, params, get_client(ctx))
