from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, DECIMAL
from app.database import Base
from datetime import datetime

class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = {"schema": "neris"}

    incident_id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("neris.departments.dept_id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("neris.shifts.shift_id"), nullable=False)
    incident_number = Column(String(20), nullable=False)
    alarm_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    arrival_time = Column(DateTime)
    cleared_time = Column(DateTime)
    business_name = Column(String(150))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(2))
    zipcode = Column(String(10))
    latitude = Column(DECIMAL(9,6))
    longitude = Column(DECIMAL(9,6))
    mutual_aid = Column(Boolean, default=False)
    narrative = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)   