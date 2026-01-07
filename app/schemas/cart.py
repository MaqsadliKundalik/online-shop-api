# app/schemas/cart.py
from typing import List, Optional
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    session_id: str
    product_id: int
    quantity: int = Field(gt=0)


class CartItemUpdate(BaseModel):
    session_id: str
    product_id: int
    quantity: int = Field(ge=0)  # 0 => o'chirish


class CartItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: int
    total_price: int

    class Config:
        orm_mode = True


class CartOut(BaseModel):
    id: Optional[int] = None
    session_id: str
    items: List[CartItemOut]
    total_price: int
