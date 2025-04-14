from pydantic import BaseModel, EmailStr
from typing import Optional


class UserResponse(BaseModel):
    message: str
    user_id: int


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: int  # 1 for admin, 2 for user
    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True
