from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from app.database import Base
from datetime import datetime

class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.station_id"), nullable=False)
    incident_type = Column(String, nullable=False)
    dspch_notes = Column(String)
    actions_taken = Column(String)
    call_time = Column(DateTime, nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.shift_id"), nullable=False)
    enrt_time = Column(DateTime)
    arrival_time = Column(DateTime)
    completed_time = Column(DateTime)
    duration_hours = Column(Float)
    response_time = Column(Float)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)   