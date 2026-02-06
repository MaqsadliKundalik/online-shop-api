from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    # YANGI: optional customer_id
    customer_id: Optional[int] = None

    # Agar customer_id berilsa va o'ziga buyurtma qilsa,
    # ism/telefon/address bo'sh bo'lishi mumkin – server o'zi to'ldiradi.
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    address: Optional[str] = None

    items: List[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    unit_price: int
    quantity: int
    total_price: int
    image: Optional[str] = None

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: int
    customer_id: Optional[int] = None
    customer_name: str
    customer_phone: str
    address: str
    status: str
    total_price: int
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
