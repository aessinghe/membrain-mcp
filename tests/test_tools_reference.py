"""Tests for src/tools/reference.py business logic (independent of FastMCP wiring)."""

from __future__ import annotations

import httpx
import respx

from src.membrain_client import MembrainClient
from src.tools.reference import _list_custom_fields, _list_processes, _list_users
from tests.conftest import BASE_URL


@respx.mock
async def test_list_users_returns_flat_list(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}users/").mock(
        return_value=httpx.Response(
            200,
            json=[
                {"Id": "u1", "Name": "Al Pacino (Hawaii)", "EmailAddress": "al@membrain.com"},
                {"Id": "u2", "Name": "Alicia Vikander", "EmailAddress": "alicia@membrain.com"},
            ],
        )
    )

    result = await _list_users(client)

    assert len(result) == 2
    assert result[0]["Name"] == "Al Pacino (Hawaii)"


@respx.mock
async def test_list_processes_dispatches_to_sales_processes_endpoint(
    client: MembrainClient,
) -> None:
    route = respx.get(f"{BASE_URL}salesProcesses/").mock(
        return_value=httpx.Response(
            200, json=[{"Id": "sp1", "Name": "Sales Process", "Stages": []}]
        )
    )

    result = await _list_processes("sales", client)

    assert route.called
    assert result[0]["Name"] == "Sales Process"


@respx.mock
async def test_list_processes_dispatches_to_flow_processes_endpoint(
    client: MembrainClient,
) -> None:
    route = respx.get(f"{BASE_URL}flowProcesses/").mock(
        return_value=httpx.Response(
            200, json=[{"Id": "fp1", "Name": "Flow Process", "ParentClass": "Company"}]
        )
    )

    result = await _list_processes("flow", client)

    assert route.called
    assert result[0]["ParentClass"] == "Company"


@respx.mock
async def test_list_custom_fields_groups_by_object_type(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}customFields/").mock(
        return_value=httpx.Response(
            200,
            json={
                "companyCustomFields": [
                    {"Id": "cf1", "Name": "Company Text Field", "Type": "Text"}
                ],
                "contactCustomFields": [],
                "userCustomFields": [],
                "activityCustomFields": [],
                "documentCustomFields": [],
                "processCustomFields": [],
            },
        )
    )

    result = await _list_custom_fields(client)

    assert result["companyCustomFields"][0]["Name"] == "Company Text Field"
    assert result["contactCustomFields"] == []
