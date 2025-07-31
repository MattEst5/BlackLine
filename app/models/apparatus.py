from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Apparatus(Base):
    __tablename__ = "apparatus"
    __table_args__ = {"schema": "neris"}

    unit_id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("neris.departments.dept_id"), nullable=False)
    unit_name = Column(String(50), unique=True, nullable=False)
    type = Column(String(50))
    status = Column(String(20), default="in_service")