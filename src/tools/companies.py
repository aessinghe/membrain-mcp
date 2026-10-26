"""MCP tools for the Membrain Company object (GET/POST/PUT /companies/).

Each tool is a thin wrapper around a plain async function (`_search_companies`,
`_get_company`, ...) that takes a `MembrainClient` directly. This keeps the actual
logic unit-testable without depending on FastMCP's decorator/Context internals.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Context, FastMCP

from src.membrain_client import MembrainClient
from src.models.common import merge_custom_fields
from src.models.company import Company, CompanyCreate, CompanySearchParams, CompanyUpdate
from src.tools._shared import dump, dump_params, get_client, paged_dump


async def _search_companies(params: CompanySearchParams, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get("companies/", params=dump_params(params))
    return paged_dump(raw, Company)


async def _get_company(company_id: str, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get(f"companies/{company_id}")
    return dump(Company.model_validate(raw))


async def _create_company(params: CompanyCreate, client: MembrainClient) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.post("companies/", json=payload)
    return dump(Company.model_validate(raw))


async def _update_company(
    company_id: str, params: CompanyUpdate, client: MembrainClient
) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.put(f"companies/{company_id}", json=payload)
    return dump(Company.model_validate(raw))


def register(mcp: FastMCP) -> None:
    """Register all Company tools on the given FastMCP server instance."""

    @mcp.tool()
    async def search_companies(params: CompanySearchParams, ctx: Context) -> dict[str, Any]:
        """Search Companies in Membrain (GET /companies/).

        Returns a paged result: {count, from, to, items}. `items` is capped by Membrain's
        own page size; call again with `from_index` set to the previous `to` to page
        through the rest of the results.
        """
        return await _search_companies(params, get_client(ctx))

    @mcp.tool()
    async def get_company(company_id: str, ctx: Context) -> dict[str, Any]:
        """Read a single Company by its GUID (GET /companies/{Id})."""
        return await _get_company(company_id, get_client(ctx))

    @mcp.tool()
    async def create_company(params: CompanyCreate, ctx: Context) -> dict[str, Any]:
        """Create a new Company in Membrain (POST /companies/).

        Consider calling `search_companies` first to check the Company does not
        already exist, to avoid creating a duplicate.
        """
        return await _create_company(params, get_client(ctx))

    @mcp.tool()
    async def update_company(
        company_id: str, params: CompanyUpdate, ctx: Context
    ) -> dict[str, Any]:
        """Update an existing Company in Membrain (PUT /companies/{Id}).

        Only the fields provided in `params` are sent; omitted fields are left unchanged.
        """
        return await _update_company(company_id, params, get_client(ctx))
