from sqlalchemy import Column, Integer, String, DateTime 
from datetime import datetime
from app.database import Base

class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)