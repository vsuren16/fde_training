from pydantic import BaseModel


class CanonicalIncident(BaseModel):
    incident_id: str
    title: str
    category: str | None = None
    priority: int | None = None
    priority_label: str | None = None
    status: str | None = None
    team: str | None = None
    assigned_to: str | None = None
    resolution_time_hours: float | None = None
    created_at: str | None = None
    created_by: str | None = None
    updated_at: str | None = None
    updated_by: str | None = None
    closed_at: str | None = None
    closed_by: str | None = None
    description: str
    resolution_notes: str
    incident_text: str
