from sqlalchemy import Column, Integer, String
from app.database import Base

class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": "neris"}

    dept_id = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String(100), nullable=False)
    city = Column(String(100))
    state = Column(String(2))
    fips_code = Column(String(10))

