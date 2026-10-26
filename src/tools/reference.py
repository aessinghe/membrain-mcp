"""MCP tools for read-only Membrain reference/configuration data.

These endpoints are low risk (read-only) and provide the GUIDs (users, process
stages, custom field definitions) needed as inputs to the write tools in
companies.py / contacts.py / opportunities.py / activities.py.

Each tool is a thin wrapper around a plain async function that takes a
`MembrainClient` directly, keeping the logic unit-testable without depending on
FastMCP's decorator/Context internals.
"""

from __future__ import annotations

from typing import Any, Literal

from fastmcp import Context, FastMCP

from src.membrain_client import MembrainClient
from src.models.reference import CustomFieldsCatalog, ProcessDescription, User
from src.tools._shared import dump, get_client, list_dump

ProcessType = Literal["sales", "prospecting", "account_growth", "ticket", "flow"]

_PROCESS_ENDPOINTS: dict[ProcessType, str] = {
    "sales": "salesProcesses/",
    "prospecting": "prospectingProcesses/",
    "account_growth": "accountGrowthProcesses/",
    "ticket": "ticketProcesses/",
    "flow": "flowProcesses/",
}


async def _list_users(client: MembrainClient) -> list[dict[str, Any]]:
    raw = await client.get("users/")
    return list_dump(raw, User)


async def _list_processes(
    process_type: ProcessType, client: MembrainClient
) -> list[dict[str, Any]]:
    raw = await client.get(_PROCESS_ENDPOINTS[process_type])
    return list_dump(raw, ProcessDescription)


async def _list_custom_fields(client: MembrainClient) -> dict[str, Any]:
    raw = await client.get("customFields/")
    return dump(CustomFieldsCatalog.model_validate(raw))


def register(mcp: FastMCP) -> None:
    """Register all reference-data tools on the given FastMCP server instance."""

    @mcp.tool()
    async def list_users(ctx: Context) -> list[dict[str, Any]]:
        """List all Membrain Users (GET /users/), sorted by Name.

        Use this to resolve an OwnerId / OpportunityOwnerId / OrganizerId GUID from a
        person's name before creating or updating an Opportunity, Note or Task.
        """
        return await _list_users(get_client(ctx))

    @mcp.tool()
    async def list_processes(process_type: ProcessType, ctx: Context) -> list[dict[str, Any]]:
        """List active Membrain Processes of the given type, including their Stages,
        Steps and Custom Field definitions.

        `process_type` selects the underlying endpoint:
          - "sales" -> GET /salesProcesses/
          - "prospecting" -> GET /prospectingProcesses/
          - "account_growth" -> GET /accountGrowthProcesses/
          - "ticket" -> GET /ticketProcesses/
          - "flow" -> GET /flowProcesses/

        Use this to discover a ProcessId before creating an Opportunity/Prospect/
        Ticket/Flow, and to learn which Custom Fields are available for that process.
        """
        return await _list_processes(process_type, get_client(ctx))

    @mcp.tool()
    async def list_custom_fields(ctx: Context) -> dict[str, Any]:
        """Fetch all Custom Field definitions in this Membrain instance (GET /customFields/),
        grouped by the object type they apply to (Company, Contact, User, Activity,
        Document, Process).

        Use this to discover a Custom Field's GUID, Type and (for Select fields) its
        Options before setting it via a `custom_fields` argument on a write tool.
        """
        return await _list_custom_fields(get_client(ctx))
