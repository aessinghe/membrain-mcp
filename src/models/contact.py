"""Models for the Membrain `Contact` object (GET/POST/PUT /contacts/)."""

from __future__ import annotations

from pydantic import Field

from src.models.common import MembrainInputModel, MembrainModel


class Contact(MembrainModel):
    """A Membrain Contact (Person) as returned by GET /contacts/ and GET /contacts/{Id}."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    first_name: str | None = Field(default=None, alias="FirstName")
    last_name: str | None = Field(default=None, alias="LastName")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    company_id: str | None = Field(default=None, alias="CompanyId")
    company_name: str | None = Field(default=None, alias="CompanyName")
    position: str | None = Field(default=None, alias="Position")
    retired: str | None = Field(default=None, alias="Retired")
    notes: str | None = Field(default=None, alias="Notes")
    work_phone: str | None = Field(default=None, alias="WorkPhone")
    cellular_phone: str | None = Field(default=None, alias="CellularPhone")
    home_phone: str | None = Field(default=None, alias="HomePhone")
    city: str | None = Field(default=None, alias="City")
    country_name: str | None = Field(default=None, alias="CountryName")
    linked_in: str | None = Field(default=None, alias="LinkedIn")
    label_ids: str | None = Field(default=None, alias="LabelIds")
    label_names: str | None = Field(default=None, alias="LabelNames")
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    reports_to_person_id: str | None = Field(default=None, alias="ReportsToPersonId")
    secondary_email_addresses: str | None = Field(default=None, alias="SecondaryEmailAddresses")
    created_date: str | None = Field(default=None, alias="CreatedDate")
    changed_date: str | None = Field(default=None, alias="ChangedDate")


class ContactSearchParams(MembrainInputModel):
    """Query filters for GET /contacts/, as documented."""


    selection_id: str | None = Field(default=None, alias="SelectionId")
    company_id: str | None = Field(default=None, alias="CompanyId")
    name: str | None = Field(default=None, alias="Name")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    phone_number: str | None = Field(
        default=None,
        alias="PhoneNumber",
        description="Exact match by default; supports optional wildcards, e.g. '555*'.",
    )
    linked_in: str | None = Field(default=None, alias="LinkedIn")
    include_retired: bool | None = Field(default=None, alias="IncludeRetired")
    has_label: str | None = Field(default=None, alias="HasLabel")
    does_not_have_label: str | None = Field(default=None, alias="DoesNotHaveLabel")
    created_by_id: str | None = Field(default=None, alias="CreatedById")
    created_from_date: str | None = Field(default=None, alias="CreatedFromDate")
    created_to_date: str | None = Field(default=None, alias="CreatedToDate")
    changed_by_id: str | None = Field(default=None, alias="ChangedById")
    changed_from_date: str | None = Field(default=None, alias="ChangedFromDate")
    changed_to_date: str | None = Field(default=None, alias="ChangedToDate")
    include_deleted: bool | None = Field(default=None, alias="IncludeDeleted")
    sort_by: str | None = Field(default=None, alias="SortBy")
    return_fields: str | None = Field(default=None, alias="Return")
    from_index: int | None = Field(default=None, alias="From")


class ContactCreate(MembrainInputModel):
    """Writable fields for POST /contacts/. Every Contact must belong to a Company."""


    first_name: str | None = Field(default=None, alias="FirstName")
    last_name: str | None = Field(default=None, alias="LastName")
    company_id: str = Field(alias="CompanyId")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    position: str | None = Field(default=None, alias="Position")
    cellular_phone: str | None = Field(default=None, alias="CellularPhone")
    work_phone: str | None = Field(default=None, alias="WorkPhone")
    notes: str | None = Field(default=None, alias="Notes")
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )


class ContactUpdate(MembrainInputModel):
    """Writable fields for PUT /contacts/{Id}. All fields are optional (partial update)."""


    name: str | None = Field(default=None, alias="Name")
    first_name: str | None = Field(default=None, alias="FirstName")
    last_name: str | None = Field(default=None, alias="LastName")
    company_id: str | None = Field(default=None, alias="CompanyId")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    secondary_email_addresses: str | None = Field(default=None, alias="SecondaryEmailAddresses")
    position: str | None = Field(default=None, alias="Position")
    work_phone: str | None = Field(default=None, alias="WorkPhone")
    cellular_phone: str | None = Field(default=None, alias="CellularPhone")
    street_address: str | None = Field(default=None, alias="StreetAddress")
    city: str | None = Field(default=None, alias="City")
    state: str | None = Field(default=None, alias="State")
    zip_code: str | None = Field(default=None, alias="ZipCode")
    notes: str | None = Field(default=None, alias="Notes")
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )
