from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__="users"

    dept_id = Column(Integer, ForeignKey("departments.dept_id"), nullable=False)
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)

    