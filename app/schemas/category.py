# app/schemas/category.py
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    unit_type: str


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
