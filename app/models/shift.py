from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Shift(Base):
    __tablename__ = "shifts"
    __table_args__ = {"schema": "neris"}

    shift_id = Column(Integer, primary_key=True, index=True)
    dept_id = Column(Integer, ForeignKey("neris.departments.dept_id"), nullable=False)
    shift_name = Column(String(20), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

class ShiftRoster(Base):
    __tablename__ = "shift_rosters"
    __table_args__ = {"schema": "neris"}

    roster_id = Column(Integer, primary_key=True, index=True)
    shift_id = Column(Integer, ForeignKey("neris.shifts.shift_id"), nullable=False)
    shift_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("neris.users.user_id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("neris.apparatus.unit_id"))
    unit_task = Column(String(50))