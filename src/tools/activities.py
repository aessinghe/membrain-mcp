"""MCP tools for creating Membrain Activities.

V1 only exposes the additive, low-risk operations: logging a Note and creating a
Task. Updating/completing/deleting activities, and creating Appointments/Calls, are
left for a later version (see project plan / README "Extensibility").

Each tool is a thin wrapper around a plain async function that takes a
`MembrainClient` directly, keeping the logic unit-testable without depending on
FastMCP's decorator/Context internals.
"""

from __future__ import annotations

from typing import Any

from fastmcp import Context, FastMCP

from src.membrain_client import MembrainClient
from src.models.activity import Activity, NoteCreate, TaskCreate
from src.models.common import merge_custom_fields
from src.tools._shared import dump, dump_params, get_client


async def _create_note(params: NoteCreate, client: MembrainClient) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.post("notes/", json=payload)
    return dump(Activity.model_validate(raw))


async def _create_task(params: TaskCreate, client: MembrainClient) -> dict[str, Any]:
    payload = merge_custom_fields(dump_params(params), params.custom_fields)
    raw = await client.post("tasks/", json=payload)
    return dump(Activity.model_validate(raw))


def register(mcp: FastMCP) -> None:
    """Register all Activity tools on the given FastMCP server instance."""

    @mcp.tool()
    async def create_note(params: NoteCreate, ctx: Context) -> dict[str, Any]:
        """Log a Note in Membrain (POST /notes/).

        `organizer_id` (the Contact/User who is the author) is required. Use
        `relateds` to attach the Note to a Company/Prospect/Opportunity/Ticket by GUID
        (comma separated for multiple).
        """
        return await _create_note(params, get_client(ctx))

    @mcp.tool()
    async def create_task(params: TaskCreate, ctx: Context) -> dict[str, Any]:
        """Create a Task in Membrain (POST /tasks/).

        `organizer_id` (the Contact/User the Task is assigned from) is required. Use
        `relateds` to attach the Task to a Company/Prospect/Opportunity/Ticket by GUID
        (comma separated for multiple).
        """
        return await _create_task(params, get_client(ctx))
