"""Tests for src/tools/contacts.py business logic (independent of FastMCP wiring)."""

from __future__ import annotations

import json

import httpx
import respx

from src.membrain_client import MembrainClient
from src.models.contact import ContactCreate, ContactSearchParams, ContactUpdate
from src.tools.contacts import _create_contact, _get_contact, _search_contacts, _update_contact
from tests.conftest import BASE_URL


@respx.mock
async def test_search_contacts_filters_by_company_id(client: MembrainClient) -> None:
    route = respx.get(f"{BASE_URL}contacts/").mock(
        return_value=httpx.Response(200, json={"count": 0, "from": 0, "to": 0, "items": []})
    )

    await _search_contacts(ContactSearchParams(company_id="c1"), client)

    assert route.calls.last.request.url.params["CompanyId"] == "c1"


@respx.mock
async def test_get_contact_returns_serialized_model(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}contacts/p1").mock(
        return_value=httpx.Response(200, json={"Id": "p1", "Name": "Alicia Vikander"})
    )

    result = await _get_contact("p1", client)

    assert result == {"Id": "p1", "Name": "Alicia Vikander"}


@respx.mock
async def test_create_contact_requires_company_id_and_merges_custom_fields(
    client: MembrainClient,
) -> None:
    route = respx.post(f"{BASE_URL}contacts/").mock(
        return_value=httpx.Response(201, json={"Id": "p1", "FirstName": "Ed"})
    )
    params = ContactCreate(
        first_name="Ed",
        last_name="Shane",
        company_id="c1",
        custom_fields={"e5f959b4-0522-4a2a-9941-950ed45217c5": "Lorem Ipsum"},
    )

    await _create_contact(params, client)

    sent_json = json.loads(route.calls.last.request.content)
    assert sent_json["CompanyId"] == "c1"
    assert sent_json["CustomFielde5f959b4-0522-4a2a-9941-950ed45217c5"] == "Lorem Ipsum"


@respx.mock
async def test_update_contact_sends_only_provided_fields(client: MembrainClient) -> None:
    route = respx.put(f"{BASE_URL}contacts/p1").mock(
        return_value=httpx.Response(200, json={"Id": "p1", "Position": "SDR"})
    )

    await _update_contact("p1", ContactUpdate(position="SDR"), client)

    sent_json = json.loads(route.calls.last.request.content)
    assert sent_json == {"Position": "SDR"}
