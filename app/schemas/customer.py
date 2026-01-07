# app/schemas/customer.py
from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    full_name: str
    phone: str
    default_address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True
