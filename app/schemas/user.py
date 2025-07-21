from pydantic import BaseModel

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

