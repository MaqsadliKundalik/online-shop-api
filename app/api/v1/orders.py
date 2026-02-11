from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderOut

# app/api/v1/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter()


@router.post("/orders", response_model=OrderOut)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
):
    """
    Buyurtma yaratish.

    Variantlar:
    1) Faqat customer_id yuboriladi -> server Customer ma'lumotlari bilan to'ldiradi
    2) customer_id + boshqa ism/telefon/address -> boshqa odam uchun buyurtma
    3) customer_id bo'lmasa -> ism/telefon/address majburiy
    """
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    customer: Customer | None = None

    if payload.customer_id is not None:
        customer = db.query(Customer).filter(Customer.id == payload.customer_id).first()
        if not customer:
            raise HTTPException(status_code=400, detail="Customer not found")
        name = payload.customer_name or customer.full_name
        phone = payload.customer_phone or customer.phone
        address = payload.address or customer.default_address
    else:
        name = payload.customer_name
        phone = payload.customer_phone
        address = payload.address

    if not name or not phone or not address:
        raise HTTPException(
            status_code=400,
            detail="Customer name, phone and address are required",
        )

    product_ids = {item.product_id for item in payload.items}
    products = (
        db.query(Product)
        .filter(Product.id.in_(product_ids), Product.status == "active")
        .all()
    )
    products_map = {p.id: p for p in products}

    if len(products_map) != len(product_ids):
        raise HTTPException(status_code=400, detail="One or more products not found or inactive")

    order = Order(
        customer_id=payload.customer_id,
        customer_name=name,
        customer_phone=phone,
        address=address,
        status="new",
        total_price=0,
    )
    db.add(order)
    db.flush()

    total_price = 0
    for item in payload.items:
        product = products_map[item.product_id]
        unit_price = product.price
        line_total = unit_price * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            unit_price=unit_price,
            quantity=item.quantity,
            total_price=line_total,
        )
        db.add(order_item)
        total_price += line_total

    order.total_price = total_price
    db.add(order)
    db.commit()
    db.refresh(order)

    return order



@router.get(
    "/orders/history",
    response_model=List[OrderOut],
    summary="Mijozning buyurtma tarixini olish",
    responses={
        200: {
            "description": "Muvaffaqiyatli javob",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1024,
                            "customer_id": 55,
                            "customer_name": "Gulnoza",
                            "customer_phone": "+998901234567",
                            "address": "Tashkent, Chilanzar",
                            "status": "confirmed",
                            "total_price": 12000000,
                            "created_at": "2023-11-15T10:30:00",
                            "items": [
                                {
                                    "id": 501,
                                    "product_id": 12,
                                    "product_name": "iPhone 15 Pro",
                                    "unit_price": 12000000,
                                    "quantity": 1,
                                    "total_price": 12000000,
                                    "image": "/static/products/iphone15.jpg"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
)
def get_order_history(
    customer_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """
    Mijozning buyurtma tarixini olish.
    """
    orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
