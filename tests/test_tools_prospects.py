"""Tests for src/tools/prospects.py business logic (independent of FastMCP wiring)."""

from __future__ import annotations

import httpx
import respx

from src.membrain_client import MembrainClient
from src.models.prospect import ProspectSearchParams
from src.tools.prospects import _get_prospect, _search_prospects
from tests.conftest import BASE_URL


@respx.mock
async def test_search_prospects_filters_by_key(client: MembrainClient) -> None:
    route = respx.get(f"{BASE_URL}prospects/").mock(
        return_value=httpx.Response(200, json={"count": 0, "from": 0, "to": 0, "items": []})
    )

    await _search_prospects(ProspectSearchParams(key="P-123"), client)

    assert route.calls.last.request.url.params["Key"] == "P-123"


@respx.mock
async def test_get_prospect_returns_serialized_model(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}prospects/pr1").mock(
        return_value=httpx.Response(200, json={"Id": "pr1", "Name": "Mozilla", "Status": "Open"})
    )

    result = await _get_prospect("pr1", client)

    assert result == {"Id": "pr1", "Name": "Mozilla", "Status": "Open"}
