"""Models for Membrain Activities. V1 only exposes creating Notes and Tasks (additive,
low-risk operations), not Appointments/Calls/Emails nor any update/delete.
"""

from __future__ import annotations

from pydantic import Field

from src.models.common import MembrainInputModel, MembrainModel


class Activity(MembrainModel):
    """An Activity (Note, Task, Appointment, Call or Email) as returned by Membrain."""

    id: str | None = Field(default=None, alias="Id")
    type: str | None = Field(default=None, alias="Type")
    activity_type_id: str | None = Field(default=None, alias="ActivityTypeId")
    activity_type_name: str | None = Field(default=None, alias="ActivityTypeName")
    subject: str | None = Field(default=None, alias="Subject")
    contents: str | None = Field(default=None, alias="Contents")
    completed: str | None = Field(default=None, alias="Completed")
    completed_date: str | None = Field(default=None, alias="CompletedDate")
    organizer_id: str | None = Field(default=None, alias="OrganizerId")
    private: str | None = Field(default=None, alias="Private")
    location: str | None = Field(default=None, alias="Location")
    from_date: str | None = Field(default=None, alias="FromDate")
    to_date: str | None = Field(default=None, alias="ToDate")
    deadline: str | None = Field(default=None, alias="Deadline")
    participants: list[dict[str, str]] | None = Field(default=None, alias="Participants")
    relateds: list[dict[str, str]] | None = Field(default=None, alias="Relateds")
    created_date: str | None = Field(default=None, alias="CreatedDate")
    changed_date: str | None = Field(default=None, alias="ChangedDate")


class NoteCreate(MembrainInputModel):
    """Writable fields for POST /notes/.

    OrganizerId is required by Membrain. Relateds/Participants are comma separated
    GUID strings (per the documented write format), not JSON arrays.
    """


    contents: str = Field(alias="Contents")
    organizer_id: str = Field(
        alias="OrganizerId", description="GUID of the Contact/User that is the organizer."
    )
    date: str | None = Field(
        default=None, alias="Date", description="Date for the Note in UTC."
    )
    relateds: str | None = Field(
        default=None,
        alias="Relateds",
        description="Comma separated GUIDs of Companies/Prospects/Opportunities/"
        "AccountGrowthItems/Tickets this Note relates to.",
    )
    participants: str | None = Field(
        default=None,
        alias="Participants",
        description="Comma separated GUIDs of participants (OrganizerId may be repeated here "
        "but must also be set separately).",
    )
    activity_type_id: str | None = Field(default=None, alias="ActivityTypeId")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )


class TaskCreate(MembrainInputModel):
    """Writable fields for POST /tasks/.

    OrganizerId is required by Membrain. Relateds/Participants are comma separated
    GUID strings (per the documented write format), not JSON arrays.
    """


    contents: str = Field(alias="Contents")
    organizer_id: str = Field(
        alias="OrganizerId", description="GUID of the Contact/User that is the organizer."
    )
    deadline: str | None = Field(
        default=None, alias="Deadline", description="Deadline for the Task in UTC."
    )
    relateds: str | None = Field(
        default=None,
        alias="Relateds",
        description="Comma separated GUIDs of Companies/Prospects/Opportunities/"
        "AccountGrowthItems/Tickets this Task relates to.",
    )
    participants: str | None = Field(
        default=None,
        alias="Participants",
        description="Comma separated GUIDs of participants (OrganizerId may be repeated here "
        "but must also be set separately).",
    )
    activity_type_id: str | None = Field(default=None, alias="ActivityTypeId")
    custom_fields: dict[str, str] | None = Field(
        default=None,
        description="Maps a Custom Field GUID (no prefix needed) to its value.",
    )
