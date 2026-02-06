# app/schemas/product.py
from pydantic import BaseModel
from typing import Optional

from app.schemas.category import CategoryOut


class ProductBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    status: str
    is_top: bool
    image_path: Optional[str] = None


class ProductOut(ProductBase):
    id: int
    category: CategoryOut
    image: Optional[str] = None

    class Config:
        orm_mode = True
