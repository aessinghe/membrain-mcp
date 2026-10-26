"""Tests for src/tools/opportunities.py business logic (independent of FastMCP wiring)."""

from __future__ import annotations

import json

import httpx
import respx

from src.membrain_client import MembrainClient
from src.models.opportunity import OpportunityCreate, OpportunitySearchParams, OpportunityUpdate
from src.tools.opportunities import (
    _create_opportunity,
    _get_opportunity,
    _search_opportunities,
    _update_opportunity,
)
from tests.conftest import BASE_URL


@respx.mock
async def test_search_opportunities_filters_by_status(client: MembrainClient) -> None:
    route = respx.get(f"{BASE_URL}opportunities/").mock(
        return_value=httpx.Response(200, json={"count": 0, "from": 0, "to": 0, "items": []})
    )

    await _search_opportunities(OpportunitySearchParams(status="Open"), client)

    assert route.calls.last.request.url.params["Status"] == "Open"


@respx.mock
async def test_get_opportunity_returns_serialized_model(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}opportunities/o1").mock(
        return_value=httpx.Response(200, json={"Id": "o1", "Name": "Air Solution"})
    )

    result = await _get_opportunity("o1", client)

    assert result == {"Id": "o1", "Name": "Air Solution"}


@respx.mock
async def test_create_opportunity_requires_process_and_owner(client: MembrainClient) -> None:
    route = respx.post(f"{BASE_URL}opportunities/").mock(
        return_value=httpx.Response(201, json={"Id": "o1", "Name": "First Sales Project"})
    )
    params = OpportunityCreate(
        name="First Sales Project",
        company_id="c1",
        process_id="p1",
        opportunity_owner_id="u1",
    )

    await _create_opportunity(params, client)

    sent_json = json.loads(route.calls.last.request.content)
    assert sent_json == {
        "Name": "First Sales Project",
        "CompanyId": "c1",
        "ProcessId": "p1",
        "OpportunityOwnerId": "u1",
    }


@respx.mock
async def test_update_opportunity_sends_only_provided_fields(client: MembrainClient) -> None:
    route = respx.put(f"{BASE_URL}opportunities/o1").mock(
        return_value=httpx.Response(200, json={"Id": "o1", "Status": "Won"})
    )

    await _update_opportunity("o1", OpportunityUpdate(status="Won"), client)

    sent_json = json.loads(route.calls.last.request.content)
    assert sent_json == {"Status": "Won"}
