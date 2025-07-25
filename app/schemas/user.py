from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    dept_id: int 
    username: str
    password: str
    full_name: str
    email: str

class UserRead(BaseModel):
    dept_id: int
    user_id: int
    username: str
    full_name: str
    email: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True


