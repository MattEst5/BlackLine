from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__="users"
    __table_args__ = {"schema": "neris"}

    user_id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("neris.departments.dept_id"), nullable=False)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    status = Column(String, default="active")
    hire_date = Column(Date)
    rank = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)

    