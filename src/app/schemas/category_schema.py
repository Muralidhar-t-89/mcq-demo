from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class Category(BaseModel):
    id: int
    name: str
    created_by: int

    class Config:
        orm_mode = True
