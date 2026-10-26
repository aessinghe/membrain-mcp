"""Helpers shared by every tools/*.py module: client access and (de)serialization."""

from __future__ import annotations

from typing import Any, TypeVar

from fastmcp import Context

from src.context import AppContext
from src.membrain_client import MembrainClient
from src.models.common import MembrainInputModel, MembrainModel

T = TypeVar("T", bound=MembrainModel)


def get_client(ctx: Context) -> MembrainClient:
    """Fetch the shared MembrainClient set up by the server's lifespan."""
    if ctx.request_context is None:
        raise RuntimeError("Tool called outside of an active MCP request context.")
    app_ctx: AppContext = ctx.request_context.lifespan_context
    return app_ctx.client


def dump(model: MembrainModel) -> dict[str, Any]:
    """Serialize a model back to Membrain's own field names, dropping unset values."""
    return model.model_dump(by_alias=True, exclude_none=True)


def dump_params(model: MembrainInputModel) -> dict[str, Any]:
    """Serialize an input model to query/body parameters using Membrain's field names."""
    return model.model_dump(by_alias=True, exclude_none=True, exclude={"custom_fields"})


def list_dump(raw: list[Any], item_model: type[T]) -> list[dict[str, Any]]:
    """Parse a flat (non-paged) Membrain JSON array endpoint into serialized items."""
    return [dump(item_model.model_validate(item)) for item in raw]


def paged_dump(raw: dict[str, Any], item_model: type[T]) -> dict[str, Any]:
    """Parse a Membrain paged envelope and re-serialize its items for the tool's output."""
    items_raw = raw.get("items") or []
    items = [item_model.model_validate(item) for item in items_raw]
    return {
        "count": int(raw.get("count", 0)),
        "from": int(raw.get("from", 0)),
        "to": int(raw.get("to", 0)),
        "items": [dump(item) for item in items],
    }
