# app/api/v1/cart.py
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartOut,
    CartItemOut,
)

router = APIRouter()


def _get_or_create_cart(db: Session, session_id: str) -> Cart:
    cart = (
        db.query(Cart)
        .filter(Cart.session_id == session_id, Cart.status == "open")
        .first()
    )
    if cart:
        return cart

    cart = Cart(session_id=session_id, status="open")
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def _build_cart_out(cart: Optional[Cart], session_id: str) -> CartOut:
    if not cart:
        return CartOut(id=None, session_id=session_id, items=[], total_price=0)

    items_out: List[CartItemOut] = []
    total_price = 0

    for item in cart.items:
        line_total = item.unit_price * item.quantity
        total_price += line_total
        items_out.append(
            CartItemOut(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product.name if item.product else "",
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=line_total,
                image=item.image,
            )
        )

    return CartOut(
        id=cart.id,
        session_id=cart.session_id or session_id,
        items=items_out,
        total_price=total_price,
    )


@router.get("/cart", response_model=CartOut)
def get_cart(
    session_id: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Foydalanuvchining ochiq savatini qaytaradi.
    Agar savat bo'lmasa — bo'sh savat qaytaradi.
    """
    cart = (
        db.query(Cart)
        .filter(Cart.session_id == session_id, Cart.status == "open")
        .first()
    )
    return _build_cart_out(cart, session_id)


@router.post("/cart/items", response_model=CartOut)
def add_or_update_cart_item(
    payload: CartItemCreate,
    db: Session = Depends(get_db),
):
    """
    Savatga mahsulot qo'shish yoki sonini o'zgartirish.

    Agar shu mahsulot savatga allaqachon qo'shilgan bo'lsa — quantity yangilanadi.
    """
    # mahsulotni tekshiramiz
    product = (
        db.query(Product)
        .filter(Product.id == payload.product_id, Product.status == "active")
        .first()
    )
    if not product:
        raise HTTPException(status_code=400, detail="Product not found or inactive")

    cart = _get_or_create_cart(db, payload.session_id)

    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == payload.product_id,
        )
        .first()
    )

    if item:
        # mavjud bo'lsa sonini yangilaymiz
        item.quantity = payload.quantity
        item.unit_price = product.price  # hozirgi narxni yangilab qo'yish mumkin
    else:
        # yangi item
        item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=payload.quantity,
            unit_price=product.price,
        )
        db.add(item)

    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart, payload.session_id)


@router.patch("/cart/items", response_model=CartOut)
def update_cart_item(
    payload: CartItemUpdate,
    db: Session = Depends(get_db),
):
    """
    CartItem quantity'ni yangilash.
    quantity = 0 bo'lsa — item o'chiriladi.
    """
    cart = (
        db.query(Cart)
        .filter(Cart.session_id == payload.session_id, Cart.status == "open")
        .first()
    )
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == payload.product_id,
        )
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if payload.quantity == 0:
        db.delete(item)
    else:
        item.quantity = payload.quantity

    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart, payload.session_id)


@router.delete("/cart/items/{item_id}", response_model=CartOut)
def delete_cart_item(
    item_id: int,
    session_id: str = Query(...),
    db: Session = Depends(get_db),
):
    cart = (
        db.query(Cart)
        .filter(Cart.session_id == session_id, Cart.status == "open")
        .first()
    )
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart, session_id)


@router.delete("/cart", response_model=CartOut)
def clear_cart(
    session_id: str = Query(...),
    db: Session = Depends(get_db),
):
    cart = (
        db.query(Cart)
        .filter(Cart.session_id == session_id, Cart.status == "open")
        .first()
    )
    if not cart:
        # bo'sh savat qaytaramiz
        return CartOut(id=None, session_id=session_id, items=[], total_price=0)

    # barcha itemlarni o'chiramiz
    for item in list(cart.items):
        db.delete(item)

    db.commit()
    db.refresh(cart)
    return _build_cart_out(cart, session_id)
