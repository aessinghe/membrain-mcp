"""Shared model building blocks used across every Membrain object model.

Design notes (per Membrain's API documentation):
  * Membrain serializes virtually every field as a JSON string, including what are
    conceptually numbers, booleans, GUIDs, and dates (e.g. Value: "180758",
    Deleted: "true", ProcessEndedDate: "1753-01-01 00:00:00.000000" as the "empty"
    sentinel). Business model fields are therefore typed as `str | None` throughout
    rather than int/float/bool/datetime, so that every documented value - including
    the "empty" sentinels - round-trips faithfully without a lossy/guessed parser.
  * Every business model allows extra fields (`extra="allow"`) because objects can
    carry an arbitrary number of `CustomField{GUID}` properties that are only known
    at runtime, per-tenant (see GET /customFields/).
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

CUSTOM_FIELD_PREFIX = "CustomField"


class MembrainModel(BaseModel):
    """Base class for models that mirror a Membrain API object.

    Unrecognized keys returned by Membrain (most notably `CustomField{GUID}`
    properties) are preserved in `model_extra` instead of raising a validation
    error, and exposed conveniently via `.custom_fields`.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @property
    def custom_fields(self) -> dict[str, str]:
        """Return only the `CustomField{GUID}` entries captured as extra data."""
        extra = self.model_extra or {}
        return {k: v for k, v in extra.items() if k.startswith(CUSTOM_FIELD_PREFIX)}


class MembrainInputModel(BaseModel):
    """Base class for tool input models (search params, create/update payloads).

    Deliberately does NOT inherit from `MembrainModel`: input models use `extra="forbid"`
    (typos in arguments should fail loudly) and must not carry the `.custom_fields`
    read-only property, which would collide with the `custom_fields` convenience field
    (a plain `dict[str, str]`) used on create/update models to pass Custom Field values.
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


T = TypeVar("T", bound=MembrainModel)


class PagedResult(BaseModel, Generic[T]):
    """Envelope returned by every Membrain list/search endpoint.

    `to` is inclusive (per the Membrain "Paging" documentation): when `to == count`
    the last page has been reached. The next page can be requested by passing
    `from_index=to` on the following call.
    """

    model_config = ConfigDict(populate_by_name=True)

    count: int
    from_index: int = Field(alias="from")
    to: int
    items: list[T] = Field(default_factory=list)


def merge_custom_fields(
    payload: dict[str, Any], custom_fields: dict[str, str] | None
) -> dict[str, Any]:
    """Fold a `{guid: value}` mapping into a request payload as `CustomField{guid}` keys.

    This is a convenience layer only: Membrain's documented write format expects the
    literal `CustomField{GUID}` property name in the request body. Callers that
    already have the prefixed key may pass it directly instead of using this helper.
    """
    if not custom_fields:
        return payload
    merged = dict(payload)
    for guid, value in custom_fields.items():
        key = guid if guid.startswith(CUSTOM_FIELD_PREFIX) else f"{CUSTOM_FIELD_PREFIX}{guid}"
        merged[key] = value
    return merged
