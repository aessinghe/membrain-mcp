"""Models for Membrain reference/configuration data: users, processes, custom fields."""

from __future__ import annotations

from pydantic import Field

from src.models.common import MembrainModel


class NamedRef(MembrainModel):
    """A simple {Id, Name} pair, used for Sales Teams, Process Stages/Steps, etc."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")


class User(MembrainModel):
    """A Membrain User as returned by GET /users/."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    company_id: str | None = Field(default=None, alias="CompanyId")
    company_name: str | None = Field(default=None, alias="CompanyName")
    email_address: str | None = Field(default=None, alias="EmailAddress")
    user_interface_language: str | None = Field(default=None, alias="UserInterfaceLanguage")
    time_zone: str | None = Field(default=None, alias="TimeZone")
    sales_teams: list[NamedRef] | None = Field(default=None, alias="SalesTeams")


class ProcessStep(MembrainModel):
    """A Step within a Process Stage."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")


class ProcessStage(MembrainModel):
    """A Stage within a Process, containing zero or more Steps."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    steps: list[ProcessStep] | None = Field(default=None, alias="Steps")


class CustomFieldOption(MembrainModel):
    """A selectable option for a SingleSelect/MultiSelect Custom Field."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")


class CustomFieldDefinition(MembrainModel):
    """A Custom Field definition, as returned by GET /customFields/ or embedded in a Process."""

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    type: str | None = Field(
        default=None,
        alias="Type",
        description="One of SingleSelect, MultiSelect, Number, Text, Date, ScoreCard, "
        "Calculation, File, Link, SingleRelationship, MultiRelationship, Currency, RichText.",
    )
    options: list[CustomFieldOption] | None = Field(default=None, alias="Options")
    related_type: str | None = Field(default=None, alias="RelatedType")
    selection_id: str | None = Field(default=None, alias="SelectionId")


class ProcessDescription(MembrainModel):
    """A Sales/Prospecting/Account Growth/Ticket/Flow Process description.

    Returned by GET /salesProcesses/, /prospectingProcesses/, /accountGrowthProcesses/,
    /ticketProcesses/ and /flowProcesses/ - see the `list_processes` tool.
    """

    id: str | None = Field(default=None, alias="Id")
    name: str | None = Field(default=None, alias="Name")
    parent_class: str | None = Field(
        default=None,
        alias="ParentClass",
        description="Flow Processes only: one of None, Company, Person, User.",
    )
    stages: list[ProcessStage] | None = Field(default=None, alias="Stages")
    custom_field_definitions: list[CustomFieldDefinition] | None = Field(
        default=None, alias="CustomFields"
    )


class CustomFieldsCatalog(MembrainModel):
    """The full response of GET /customFields/, grouped by the object type they apply to."""

    company_custom_fields: list[CustomFieldDefinition] = Field(
        default_factory=list, alias="companyCustomFields"
    )
    contact_custom_fields: list[CustomFieldDefinition] = Field(
        default_factory=list, alias="contactCustomFields"
    )
    user_custom_fields: list[CustomFieldDefinition] = Field(
        default_factory=list, alias="userCustomFields"
    )
    activity_custom_fields: list[CustomFieldDefinition] = Field(
        default_factory=list, alias="activityCustomFields"
    )
    document_custom_fields: list[CustomFieldDefinition] = Field(
        default_factory=list, alias="documentCustomFields"
    )
    process_custom_fields: list[CustomFieldDefinition] = Field(
        default_factory=list, alias="processCustomFields"
    )
