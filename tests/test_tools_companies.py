"""Tests for src/tools/companies.py business logic (independent of FastMCP wiring)."""

from __future__ import annotations

import httpx
import respx

from src.membrain_client import MembrainClient
from src.models.company import CompanyCreate, CompanySearchParams, CompanyUpdate
from src.tools.companies import _create_company, _get_company, _search_companies, _update_company
from tests.conftest import BASE_URL


@respx.mock
async def test_search_companies_returns_paged_result(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}companies/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "from": 0,
                "to": 1,
                "items": [{"Id": "c1", "Name": "Acme Inc"}],
            },
        )
    )

    result = await _search_companies(CompanySearchParams(name="Acme*"), client)

    assert result["count"] == 1
    assert result["to"] == 1
    assert result["items"][0]["Name"] == "Acme Inc"


@respx.mock
async def test_search_companies_passes_name_filter_as_query_param(
    client: MembrainClient,
) -> None:
    route = respx.get(f"{BASE_URL}companies/").mock(
        return_value=httpx.Response(200, json={"count": 0, "from": 0, "to": 0, "items": []})
    )

    await _search_companies(CompanySearchParams(name="Acme*"), client)

    assert route.calls.last.request.url.params["Name"] == "Acme*"


@respx.mock
async def test_get_company_returns_serialized_model(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}companies/c1").mock(
        return_value=httpx.Response(200, json={"Id": "c1", "Name": "Acme Inc"})
    )

    result = await _get_company("c1", client)

    assert result == {"Id": "c1", "Name": "Acme Inc"}


@respx.mock
async def test_create_company_merges_custom_fields_into_payload(client: MembrainClient) -> None:
    route = respx.post(f"{BASE_URL}companies/").mock(
        return_value=httpx.Response(201, json={"Id": "c1", "Name": "Acme Inc"})
    )
    params = CompanyCreate(
        name="Acme Inc",
        custom_fields={"447dbe60-4925-4a75-b07b-13ad07d095d7": "Lorem Ipsum"},
    )

    result = await _create_company(params, client)

    sent_body = route.calls.last.request.content
    import json as _json

    sent_json = _json.loads(sent_body)
    assert sent_json["Name"] == "Acme Inc"
    assert sent_json["CustomField447dbe60-4925-4a75-b07b-13ad07d095d7"] == "Lorem Ipsum"
    assert "custom_fields" not in sent_json
    assert result["Id"] == "c1"


@respx.mock
async def test_update_company_sends_only_provided_fields(client: MembrainClient) -> None:
    route = respx.put(f"{BASE_URL}companies/c1").mock(
        return_value=httpx.Response(200, json={"Id": "c1", "Name": "Acme Renamed"})
    )

    await _update_company("c1", CompanyUpdate(name="Acme Renamed"), client)

    import json as _json

    sent_json = _json.loads(route.calls.last.request.content)
    assert sent_json == {"Name": "Acme Renamed"}
