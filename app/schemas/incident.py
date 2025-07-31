from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IncidentBase(BaseModel):
    incident_number: str
    shift_id: int
    business_name: str
    address: str
    city: str
    state: str
    zipcode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    narrative: Optional[str] = None
    mutual_aid: bool = False

class IncidentCreate(IncidentBase):
    alarm_time: Optional[datetime] = None

class IncidentRead(IncidentBase):
    incident_id: int
    dept_id: int
    alarm_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True