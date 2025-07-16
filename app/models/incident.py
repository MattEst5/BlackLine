from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base
from datetime import datetime 

class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(String, nullable=False)
    station_id = Column(Integer, nullable=False)
    dspch_notes = Column(String)
    actions_taken = Column(String)
    call_time = Column(DateTime, nullable=False)
    enrt_time = Column(DateTime)
    arrival_time = Column(DateTime)
    completed_time = Column(DateTime)
    duration_hours = Column(Float)
    response_time = Column(Float)