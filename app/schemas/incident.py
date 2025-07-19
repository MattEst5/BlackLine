from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentBase(BaseModel):
    department_id: int
    shift_id: int
    station_id: int
    incident_type: str
    dspch_notes: Optional[str] = None
    actions_taken: Optional[str] = None
    call_time: datetime
    enrt_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    duration_hours: Optional[float] = None
    response_time: Optional[float] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentRead(IncidentBase):
    incident_id: int

    class Config:
        orm_mode = True