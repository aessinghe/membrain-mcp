"""Models for the Membrain `Prospect` object (read-only in this MCP server's V1).

GET /prospects/ and GET /prospects/{Id} are exposed; POST/PUT are deliberately left
out of V1 to keep the initial tool surface focused (see the project plan).
"""

from __future__ import annotations

from pydantic import Field

from src.models.common import MembrainInputModel, MembrainModel


class Prospect(MembrainModel):
    """A Membrain Prospect as returned by GET /prospects/{Id}."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    key: str | None = Field(default=None, alias="Key")
    company_id: str | None = Field(default=None, alias="CompanyId")
    company_name: str | None = Field(default=None, alias="CompanyName")
    prospect_owner_id: str | None = Field(default=None, alias="ProspectOwnerId")
    prospect_owner_name: str | None = Field(default=None, alias="ProspectOwnerName")
    process_id: str | None = Field(default=None, alias="ProcessId")
    process_name: str | None = Field(default=None, alias="ProcessName")
    process_current_stage_id: str | None = Field(default=None, alias="ProcessCurrentStageId")
    process_current_stage_name: str | None = Field(default=None, alias="ProcessCurrentStageName")
    process_started_date: str | None = Field(default=None, alias="ProcessStartedDate")
    process_ended_date: str | None = Field(default=None, alias="ProcessEndedDate")
    status: str | None = Field(default=None, alias="Status")
    negative_result_or_opportunity_id: str | None = Field(
        default=None, alias="NegativeResultOrOpportunityId"
    )
    negative_result_name: str | None = Field(default=None, alias="NegativeResultName")
    opportunity_name: str | None = Field(default=None, alias="OpportunityName")
    created_date: str | None = Field(default=None, alias="CreatedDate")
    changed_date: str | None = Field(default=None, alias="ChangedDate")


class ProspectSearchParams(MembrainInputModel):
    """Query filters for GET /prospects/, as documented."""


    selection_id: str | None = Field(default=None, alias="SelectionId")
    name: str | None = Field(default=None, alias="Name")
    company_id: str | None = Field(default=None, alias="CompanyId")
    person_id: str | None = Field(
        default=None, alias="PersonId", description="Find Prospects related to a given Contact."
    )
    process_id: str | None = Field(default=None, alias="ProcessId")
    owner_id: str | None = Field(default=None, alias="OwnerId")
    status: str | None = Field(
        default=None,
        alias="Status",
        description="Comma separated list of: Open, Qualified, Disqualified.",
    )
    key: str | None = Field(default=None, alias="Key", description="Ex: P-123.")
    created_by_id: str | None = Field(default=None, alias="CreatedById")
    created_from_date: str | None = Field(default=None, alias="CreatedFromDate")
    created_to_date: str | None = Field(default=None, alias="CreatedToDate")
    changed_by_id: str | None = Field(default=None, alias="ChangedById")
    changed_from_date: str | None = Field(default=None, alias="ChangedFromDate")
    changed_to_date: str | None = Field(default=None, alias="ChangedToDate")
    return_fields: str | None = Field(default=None, alias="Return")
    from_index: int | None = Field(default=None, alias="From")
