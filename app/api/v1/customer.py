# app/api/v1/customers.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerLogin

router = APIRouter()


@router.post(
    "/customers",
    response_model=CustomerOut,
    summary="Yangi mijozni ro'yxatdan o'tkazish",
    description="Full name, phone va optional default_address asosida yangi customer yaratadi.",
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
):
    # telefon bo'yicha mavjudligini tekshiramiz
    existing = db.query(Customer).filter(Customer.phone == payload.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this phone already exists")

    customer = Customer(
        full_name=payload.full_name,
        phone=payload.phone,
        default_address=payload.default_address,
    )
    customer.set_password(payload.password)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.post(
    "/customers/login",
    summary="Mijoz login qilishi",
    description="Telefon raqami va parol orqali login qilish.",
)
def login_customer(
    payload: CustomerLogin,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.phone == payload.phone).first()
    if not customer or not customer.verify_password(payload.password):
        raise HTTPException(status_code=400, detail="Phone or password incorrect")
    
    # Kelajakda JWT token qaytarish mumkin
    return {
        "status": "success",
        "message": "Login successful",
        "customer": {
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "default_address": customer.default_address,
        }
    }


@router.post(
    "/customers/logout",
    summary="Mijoz logout qilishi",
)
def logout_customer():
    # Stateless API uchun logout asosan client-side handled
    return {"status": "success", "message": "Logout successful"}


@router.get(
    "/customers/{customer_id}",
    response_model=CustomerOut,
    summary="Customer ma'lumotlarini olish",
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get(
    "/customers/by-phone",
    response_model=CustomerOut,
    summary="Telefon raqam bo'yicha customer topish",
)
def get_customer_by_phone(
    phone: str = Query(...),
    db: Session = Depends(get_db),
):
    customer = db.query(Customer).filter(Customer.phone == phone).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
