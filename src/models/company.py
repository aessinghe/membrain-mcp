"""Models for the Membrain `Company` object (GET/POST/PUT /companies/)."""

from __future__ import annotations

from pydantic import Field

from src.models.common import MembrainInputModel, MembrainModel


class Company(MembrainModel):
    """A Membrain Company as returned by GET /companies/ and GET /companies/{Id}.

    Only the most commonly used properties are declared explicitly; every other
    documented property (including the BillingAddress.*/ShippingAddress.*/
    VisitingAddress.* dotted keys and any `CustomField{GUID}`) is still present on
    the instance via `model_extra` / `.custom_fields` thanks to `extra="allow"`.
    """

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    city: str | None = Field(default=None, alias="City")
    country_name: str | None = Field(default=None, alias="CountryName")
    country_code: str | None = Field(default=None, alias="CountryCode")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    homepage: str | None = Field(default=None, alias="Homepage")
    phone: str | None = Field(default=None, alias="Phone")
    linked_in: str | None = Field(default=None, alias="LinkedIn")
    label_ids: str | None = Field(default=None, alias="LabelIds")
    label_names: str | None = Field(default=None, alias="LabelNames")
    notes: str | None = Field(default=None, alias="Notes")
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    parent_company_id: str | None = Field(default=None, alias="ParentCompanyId")
    parent_company_name: str | None = Field(default=None, alias="ParentCompanyName")
    sales_person_id: str | None = Field(default=None, alias="SalesPersonId")
    sales_person_name: str | None = Field(default=None, alias="SalesPersonName")
    state: str | None = Field(default=None, alias="State")
    street_address: str | None = Field(default=None, alias="StreetAddress")
    created_date: str | None = Field(default=None, alias="CreatedDate")
    changed_date: str | None = Field(default=None, alias="ChangedDate")
    deleted: str | None = Field(default=None, alias="Deleted")


class CompanySearchParams(MembrainInputModel):
    """Query filters for GET /companies/, as documented."""


    selection_id: str | None = Field(default=None, alias="SelectionId")
    name: str | None = Field(
        default=None, alias="Name", description="Supports optional wildcards, e.g. 'Acme*'."
    )
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    linked_in: str | None = Field(default=None, alias="LinkedIn")
    homepage: str | None = Field(default=None, alias="Homepage")
    sales_person_id: str | None = Field(
        default=None, alias="SalesPersonId", description="Comma separated list of User GUIDs."
    )
    has_label: str | None = Field(
        default=None, alias="HasLabel", description="Comma separated list of Label GUIDs."
    )
    does_not_have_label: str | None = Field(default=None, alias="DoesNotHaveLabel")
    created_by_id: str | None = Field(default=None, alias="CreatedById")
    created_from_date: str | None = Field(
        default=None,
        alias="CreatedFromDate",
        description="Format YYYY-MM-DD[ HH:mm:ss.ffffff]. Must be given with created_to_date.",
    )
    created_to_date: str | None = Field(default=None, alias="CreatedToDate")
    changed_by_id: str | None = Field(default=None, alias="ChangedById")
    changed_from_date: str | None = Field(default=None, alias="ChangedFromDate")
    changed_to_date: str | None = Field(default=None, alias="ChangedToDate")
    include_deleted: bool | None = Field(default=None, alias="IncludeDeleted")
    sort_by: str | None = Field(
        default=None,
        alias="SortBy",
        description="One of 'CreatedDate ASC', 'CreatedDate DESC', 'ChangedDate ASC', "
        "'ChangedDate DESC'. Defaults to Name ASC.",
    )
    return_fields: str | None = Field(
        default=None,
        alias="Return",
        description="Comma separated list of fields to return, to reduce payload size.",
    )
    from_index: int | None = Field(
        default=None, alias="From", description="Paging offset, per the Membrain Paging docs."
    )


class CompanyCreate(MembrainInputModel):
    """Writable fields for POST /companies/. `Name` is the only field Membrain requires."""


    name: str = Field(alias="Name")
    city: str | None = Field(default=None, alias="City")
    country_name: str | None = Field(default=None, alias="CountryName")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    homepage: str | None = Field(default=None, alias="Homepage")
    phone: str | None = Field(default=None, alias="Phone")
    linked_in: str | None = Field(default=None, alias="LinkedIn")
    facebook: str | None = Field(default=None, alias="Facebook")
    twitter: str | None = Field(default=None, alias="Twitter")
    instagram: str | None = Field(default=None, alias="Instagram")
    notes: str | None = Field(default=None, alias="Notes")
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    parent_company_id: str | None = Field(default=None, alias="ParentCompanyId")
    sales_person_id: str | None = Field(default=None, alias="SalesPersonId")
    state: str | None = Field(default=None, alias="State")
    street_address: str | None = Field(default=None, alias="StreetAddress")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )


class CompanyUpdate(MembrainInputModel):
    """Writable fields for PUT /companies/{Id}. All fields are optional (partial update)."""


    name: str | None = Field(default=None, alias="Name")
    city: str | None = Field(default=None, alias="City")
    country_name: str | None = Field(default=None, alias="CountryName")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    homepage: str | None = Field(default=None, alias="Homepage")
    phone: str | None = Field(default=None, alias="Phone")
    linked_in: str | None = Field(default=None, alias="LinkedIn")
    facebook: str | None = Field(default=None, alias="Facebook")
    twitter: str | None = Field(default=None, alias="Twitter")
    instagram: str | None = Field(default=None, alias="Instagram")
    notes: str | None = Field(default=None, alias="Notes")
    external_identifier: str | None = Field(default=None, alias="ExternalIdentifier")
    parent_company_id: str | None = Field(default=None, alias="ParentCompanyId")
    sales_person_id: str | None = Field(default=None, alias="SalesPersonId")
    state: str | None = Field(default=None, alias="State")
    street_address: str | None = Field(default=None, alias="StreetAddress")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )
