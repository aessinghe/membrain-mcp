"""MCP tools for the Membrain Contact object (GET/POST/PUT /contacts/).

Each tool is a thin wrapper around a plain async function that takes a
`MembrainClient` directly, keeping the logic unit-testable without depending on
FastMCP's decorator/Context internals.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Context, FastMCP

from src.membrain_client import MembrainClient
from src.models.common import merge_custom_fields
from src.models.contact import Contact, ContactCreate, ContactSearchParams, ContactUpdate
from src.tools._shared import dump, dump_params, get_client, paged_dump


async def _search_contacts(params: ContactSearchParams, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get("contacts/", params=dump_params(params))
    return paged_dump(raw, Contact)


async def _get_contact(contact_id: str, client: MembrainClient) -> dict[str, Any]:
    raw = await client.get(f"contacts/{contact_id}")
    return dump(Contact.model_validate(raw))


async def _create_contact(params: ContactCreate, client: MembrainClient) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.post("contacts/", json=payload)
    return dump(Contact.model_validate(raw))


async def _update_contact(
    contact_id: str, params: ContactUpdate, client: MembrainClient
) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.put(f"contacts/{contact_id}", json=payload)
    return dump(Contact.model_validate(raw))


def register(mcp: FastMCP) -> None:
    """Register all Contact tools on the given FastMCP server instance."""

    @mcp.tool()
    async def search_contacts(params: ContactSearchParams, ctx: Context) -> dict[str, Any]:
        """Search Contacts (People) in Membrain (GET /contacts/).

        Returns a paged result: {count, from, to, items}. Page further by calling again
        with `from_index` set to the previous `to`.
        """
        return await _search_contacts(params, get_client(ctx))

    @mcp.tool()
    async def get_contact(contact_id: str, ctx: Context) -> dict[str, Any]:
        """Read a single Contact by its GUID (GET /contacts/{Id})."""
        return await _get_contact(contact_id, get_client(ctx))

    @mcp.tool()
    async def create_contact(params: ContactCreate, ctx: Context) -> dict[str, Any]:
        """Create a new Contact in Membrain (POST /contacts/).

        Every Contact must belong to a Company: resolve or create it first via
        `search_companies` / `create_company`.
        """
        return await _create_contact(params, get_client(ctx))

    @mcp.tool()
    async def update_contact(
        contact_id: str, params: ContactUpdate, ctx: Context
    ) -> dict[str, Any]:
        """Update an existing Contact in Membrain (PUT /contacts/{Id}).

        Only the fields provided in `params` are sent; omitted fields are left unchanged.
        """
        return await _update_contact(contact_id, params, get_client(ctx))
