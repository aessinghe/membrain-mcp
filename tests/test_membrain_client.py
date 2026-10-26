"""Tests for src/membrain_client.py: auth, retries, error handling."""

from __future__ import annotations

import httpx
import pytest
import respx

from src.membrain_client import MembrainAPIError, MembrainClient
from tests.conftest import BASE_URL


@respx.mock
async def test_get_sends_api_key_header(client: MembrainClient) -> None:
    route = respx.get(f"{BASE_URL}companies/").mock(
        return_value=httpx.Response(200, json={"count": 0, "from": 0, "to": 0, "items": []})
    )

    result = await client.get("companies/")

    assert result == {"count": 0, "from": 0, "to": 0, "items": []}
    assert route.calls.last.request.headers["APIKey"] == "test-api-key"


@respx.mock
async def test_get_drops_none_query_params(client: MembrainClient) -> None:
    route = respx.get(f"{BASE_URL}companies/").mock(
        return_value=httpx.Response(200, json={"count": 0, "from": 0, "to": 0, "items": []})
    )

    await client.get("companies/", params={"Name": "Acme*", "SelectionId": None})

    sent_url = route.calls.last.request.url
    assert "Name=Acme" in str(sent_url)
    assert "SelectionId" not in str(sent_url)


@respx.mock
async def test_get_retries_on_transient_5xx_then_succeeds(client: MembrainClient) -> None:
    route = respx.get(f"{BASE_URL}companies/1").mock(
        side_effect=[
            httpx.Response(503, text="temporarily unavailable"),
            httpx.Response(200, json={"Id": "1", "Name": "Acme"}),
        ]
    )

    result = await client.get("companies/1")

    assert result == {"Id": "1", "Name": "Acme"}
    assert route.call_count == 2


@respx.mock
async def test_get_raises_after_exhausting_retries(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}companies/1").mock(return_value=httpx.Response(500, text="boom"))

    with pytest.raises(MembrainAPIError) as exc_info:
        await client.get("companies/1")

    assert exc_info.value.status_code == 500
    assert "boom" in exc_info.value.body


@respx.mock
async def test_post_is_never_retried_on_5xx(client: MembrainClient) -> None:
    route = respx.post(f"{BASE_URL}companies/").mock(
        return_value=httpx.Response(500, text="boom")
    )

    with pytest.raises(MembrainAPIError):
        await client.post("companies/", json={"Name": "Acme"})

    assert route.call_count == 1


@respx.mock
async def test_non_2xx_raises_membrain_api_error_with_body(client: MembrainClient) -> None:
    respx.get(f"{BASE_URL}companies/missing").mock(
        return_value=httpx.Response(404, text="Not Found")
    )

    with pytest.raises(MembrainAPIError) as exc_info:
        await client.get("companies/missing")

    assert exc_info.value.status_code == 404
    assert "Not Found" in str(exc_info.value)


@respx.mock
async def test_put_success_returns_parsed_json(client: MembrainClient) -> None:
    respx.put(f"{BASE_URL}companies/1").mock(
        return_value=httpx.Response(200, json={"Id": "1", "Name": "Updated"})
    )

    result = await client.put("companies/1", json={"Name": "Updated"})

    assert result == {"Id": "1", "Name": "Updated"}
