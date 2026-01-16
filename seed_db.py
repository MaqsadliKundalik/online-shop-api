# seed_db.py

from random import randint, choice
from faker import Faker
from app.db.session import SessionLocal
from app.models import Category, Product, Order, OrderItem, Customer
from app.models.user import AdminUser

fake = Faker("en_US")

def seed_admins(db):
    # 1. Superuser
    admin = db.query(AdminUser).filter_by(username="admin").first()
    if not admin:
        print("Creating superuser 'admin'...")
        admin = AdminUser(username="admin", is_superuser=True)
        admin.set_password("admin123")
        db.add(admin)
    
    # 2. Regular Admin
    ruslan = db.query(AdminUser).filter_by(username="ruslan").first()
    if not ruslan:
        print("Creating regular admin 'ruslan'...")
        ruslan = AdminUser(username="ruslan", is_superuser=False)
        ruslan.set_password("ruslan123")
        db.add(ruslan)
    db.commit()

def seed_customers(db, count: int = 10):
    if db.query(Customer).count() > 0:
        return
    for _ in range(count):
        customer = Customer(
            full_name=fake.name(),
            phone=fake.phone_number(),
            default_address=fake.address().replace("\n", ", "),
        )
        db.add(customer)
    db.commit()
    print(f"Created {count} customers.")

def seed_categories(db):
    if db.query(Category).count() > 0:
        return
    categories_data = [
        ("Elektronika", "piece"),
        ("Kiyim-kechak", "piece"),
        ("Oziq-ovqat", "weight"),
        ("Kitoblar", "piece"),
    ]
    for name, unit_type in categories_data:
        cat = Category(name=name, unit_type=unit_type)
        db.add(cat)
    db.commit()
    print(f"Created {len(categories_data)} categories.")

def seed_products(db, ppc: int = 10):
    if db.query(Product).count() > 0:
        return
    categories = db.query(Category).all()
    for cat in categories:
        for _ in range(ppc):
            product = Product(
                name=f"{cat.name} {fake.word().capitalize()}",
                price=randint(5000, 200000),
                description=fake.sentence(),
                status="active",
                is_top=choice([True, False]),
                category_id=cat.id
            )
            db.add(product)
    db.commit()
    print("Created fake products.")

def seed_orders(db, count: int = 15):
    if db.query(Order).count() > 0:
        return
    customers = db.query(Customer).all()
    products = db.query(Product).all()
    for _ in range(count):
        customer = choice(customers)
        order = Order(
            customer_id=customer.id,
            customer_name=customer.full_name,
            customer_phone=customer.phone,
            address=customer.default_address,
            status=choice(["new", "completed", "cancelled"]),
            total_price=0
        )
        db.add(order)
        db.flush()
        
        total = 0
        for _ in range(randint(1, 3)):
            p = choice(products)
            qty = randint(1, 5)
            item = OrderItem(
                order_id=order.id,
                product_id=p.id,
                product_name=p.name,
                unit_price=p.price,
                quantity=qty,
                total_price=p.price * qty
            )
            db.add(item)
            total += item.total_price
        order.total_price = total
    db.commit()
    print(f"Created {count} orders.")

def main():
    db = SessionLocal()
    try:
        seed_admins(db)
        seed_customers(db)
        seed_categories(db)
        seed_products(db)
        seed_orders(db)
        print("Database seeding completed.")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

