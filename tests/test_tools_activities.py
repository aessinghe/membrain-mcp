"""Tests for src/tools/activities.py business logic (independent of FastMCP wiring)."""

from __future__ import annotations

import json

import httpx
import respx

from src.membrain_client import MembrainClient
from src.models.activity import NoteCreate, TaskCreate
from src.tools.activities import _create_note, _create_task
from tests.conftest import BASE_URL


@respx.mock
async def test_create_note_requires_organizer_and_contents(client: MembrainClient) -> None:
    route = respx.post(f"{BASE_URL}notes/").mock(
        return_value=httpx.Response(201, json={"Id": "n1", "Type": "Note"})
    )
    params = NoteCreate(
        contents="Called the client, no answer.",
        organizer_id="u1",
        relateds="c1",
    )

    result = await _create_note(params, client)

    sent_json = json.loads(route.calls.last.request.content)
    assert sent_json == {
        "Contents": "Called the client, no answer.",
        "OrganizerId": "u1",
        "Relateds": "c1",
    }
    assert result == {"Id": "n1", "Type": "Note"}


@respx.mock
async def test_create_task_merges_custom_fields(client: MembrainClient) -> None:
    route = respx.post(f"{BASE_URL}tasks/").mock(
        return_value=httpx.Response(201, json={"Id": "t1", "Type": "Task"})
    )
    params = TaskCreate(
        contents="Follow up next week",
        organizer_id="u1",
        deadline="2026-01-19 03:00:00.000000",
        custom_fields={"145141d97a6d4b19bb04c0dce6946b98": "High priority"},
    )

    await _create_task(params, client)

    sent_json = json.loads(route.calls.last.request.content)
    assert sent_json["Deadline"] == "2026-01-19 03:00:00.000000"
    assert sent_json["CustomField145141d97a6d4b19bb04c0dce6946b98"] == "High priority"
    assert "custom_fields" not in sent_json
