# app/api/v1/products.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.product import Product
from app.schemas.product import ProductOut

router = APIRouter()


@router.get("/products", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None),
    is_top: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Android uchun mahsulotlar ro'yxati:
    - /products?category_id=1
    - /products?is_top=true
    - /products?search=cola
    """
    query = db.query(Product)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if is_top is not None:
        query = query.filter(Product.is_top == is_top)

    if search:
        like = f"%{search}%"
        query = query.filter(Product.name.ilike(like))

    products = query.offset(offset).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
