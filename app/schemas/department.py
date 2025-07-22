from pydantic import BaseModel
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str 

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    dept_id: int
    created_at: datetime 

    class Config:
        from_attributes = True
        