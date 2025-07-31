from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from app.database import Base

class IncidentPersonnel(Base):
    __tablename__ = "incident_personnel"
    __table_args__ = {"schema": "neris"}

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("neris.incidents.incident_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("neris.users.user_id", ondelete="CASCADE"))
    unit_id = Column(Integer, ForeignKey("neris.apparatus.unit_id"))
    unit_task = Column(String(50))
    actions_taken = Column(Text)
    