"""Models for the Membrain `Opportunity` (Sales Project) object (GET/POST/PUT /opportunities/)."""

from __future__ import annotations

from pydantic import Field

from src.models.common import MembrainInputModel, MembrainModel


class Opportunity(MembrainModel):
    """A Membrain Opportunity (Sales Project) as returned by GET /opportunities/{Id}."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    key: str | None = Field(default=None, alias="Key")
    company_id: str | None = Field(default=None, alias="CompanyId")
    company_name: str | None = Field(default=None, alias="CompanyName")
    opportunity_owner_id: str | None = Field(default=None, alias="OpportunityOwnerId")
    opportunity_owner_name: str | None = Field(default=None, alias="OpportunityOwnerName")
    process_id: str | None = Field(default=None, alias="ProcessId")
    process_name: str | None = Field(default=None, alias="ProcessName")
    process_current_stage_id: str | None = Field(default=None, alias="ProcessCurrentStageId")
    process_current_stage_name: str | None = Field(default=None, alias="ProcessCurrentStageName")
    process_started_date: str | None = Field(default=None, alias="ProcessStartedDate")
    process_ended_date: str | None = Field(default=None, alias="ProcessEndedDate")
    estimated_closing_date: str | None = Field(default=None, alias="EstimatedClosingDate")
    probability: str | None = Field(default=None, alias="Probability")
    value: str | None = Field(default=None, alias="Value")
    value_in_currency: str | None = Field(default=None, alias="ValueInCurrency")
    value_currency_code: str | None = Field(default=None, alias="ValueCurrencyCode")
    value_currency_id: str | None = Field(default=None, alias="ValueCurrencyId")
    weighted_value: str | None = Field(default=None, alias="WeightedValue")
    status: str | None = Field(default=None, alias="Status")
    lost_comment: str | None = Field(default=None, alias="LostComment")
    lost_reason_id: str | None = Field(default=None, alias="LostReasonId")
    lost_reason_name: str | None = Field(default=None, alias="LostReasonName")
    created_date: str | None = Field(default=None, alias="CreatedDate")
    changed_date: str | None = Field(default=None, alias="ChangedDate")


class OpportunitySearchParams(MembrainInputModel):
    """Query filters for GET /opportunities/, as documented."""


    selection_id: str | None = Field(default=None, alias="SelectionId")
    name: str | None = Field(default=None, alias="Name")
    company_id: str | None = Field(
        default=None, alias="CompanyId", description="Comma separated list of Company GUIDs."
    )
    process_id: str | None = Field(
        default=None, alias="ProcessId", description="Comma separated list of Sales Process GUIDs."
    )
    owner_id: str | None = Field(
        default=None, alias="OwnerId", description="Comma separated list of User GUIDs."
    )
    status: str | None = Field(
        default=None, alias="Status", description="Comma separated list of: Open, Won, Archived."
    )
    key: str | None = Field(
        default=None, alias="Key", description="Ex: SP-581. Look up the Id from a known key."
    )
    created_by_id: str | None = Field(default=None, alias="CreatedById")
    created_from_date: str | None = Field(default=None, alias="CreatedFromDate")
    created_to_date: str | None = Field(default=None, alias="CreatedToDate")
    changed_by_id: str | None = Field(default=None, alias="ChangedById")
    changed_from_date: str | None = Field(default=None, alias="ChangedFromDate")
    changed_to_date: str | None = Field(default=None, alias="ChangedToDate")
    return_fields: str | None = Field(default=None, alias="Return")
    from_index: int | None = Field(default=None, alias="From")


class OpportunityCreate(MembrainInputModel):
    """Writable fields for POST /opportunities/.

    Membrain requires at minimum Name, CompanyId, ProcessId and OpportunityOwnerId.
    Use `list_processes` to discover ProcessId and `list_users` for OpportunityOwnerId.
    """


    name: str = Field(alias="Name")
    company_id: str = Field(alias="CompanyId")
    process_id: str = Field(alias="ProcessId")
    opportunity_owner_id: str = Field(alias="OpportunityOwnerId")
    value_in_currency: str | None = Field(default=None, alias="ValueInCurrency")
    value_currency_code: str | None = Field(default=None, alias="ValueCurrencyCode")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )


class OpportunityUpdate(MembrainInputModel):
    """Writable fields for PUT /opportunities/{Id}. All fields are optional (partial update)."""


    name: str | None = Field(default=None, alias="Name")
    opportunity_owner_id: str | None = Field(default=None, alias="OpportunityOwnerId")
    opportunity_owner_name: str | None = Field(default=None, alias="OpportunityOwnerName")
    value_in_currency: str | None = Field(default=None, alias="ValueInCurrency")
    value_currency_code: str | None = Field(default=None, alias="ValueCurrencyCode")
    process_started_date: str | None = Field(default=None, alias="ProcessStartedDate")
    process_ended_date: str | None = Field(default=None, alias="ProcessEndedDate")
    status: str | None = Field(
        default=None, alias="Status", description="One of Open, Won, Archived."
    )
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )
