# scripts/seed_db.py

from random import randint, choice

from faker import Faker

from app.db.session import SessionLocal
from app.models import Category, Product, Order, OrderItem, Customer

fake = Faker("en_US")


def seed_customers(db, count: int = 5):
    existing_count = db.query(Customer).count()
    if existing_count > 0:
        print(f"Customers already exist ({existing_count} rows), skipping.")
        return

    for _ in range(count):
        full_name = fake.name()
        phone = fake.phone_number()
        address = fake.address().replace("\n", ", ")

        customer = Customer(
            full_name=full_name,
            phone=phone,
            default_address=address,
        )
        db.add(customer)

    db.commit()
    print(f"Created {count} customers.")


def seed_categories(db):
    existing_count = db.query(Category).count()
    if existing_count > 0:
        print(f"Categories already exist ({existing_count} rows), skipping.")
        return

    categories_data = [
        ("Ichimliklar", "piece"),
        ("Shirinliklar", "piece"),
        ("Mevalar", "weight"),
        ("Sabzavotlar", "weight"),
    ]

    for name, unit_type in categories_data:
        cat = Category(name=name, unit_type=unit_type)
        db.add(cat)

    db.commit()
    print(f"Created {len(categories_data)} categories.")


def seed_products(db, products_per_category: int = 5):
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"Products already exist ({existing_count} rows), skipping.")
        return

    categories = db.query(Category).all()
    if not categories:
        print("No categories found. Run seed_categories first.")
        return

    total = 0
    for cat in categories:
        for _ in range(products_per_category):
            name = f"{cat.name} - {fake.word().capitalize()}"
            price = randint(10_000, 150_000)
            description = fake.sentence(nb_words=8)

            product = Product(
                name=name,
                price=price,
                description=description,
                status="active",
                is_top=bool(randint(0, 1)),
                category_id=cat.id,
                image_path=None,
            )
            db.add(product)
            total += 1

    db.commit()
    print(f"Created {total} products.")


def seed_orders(db, orders_count: int = 3):
    existing_count = db.query(Order).count()
    if existing_count > 0:
        print(f"Orders already exist ({existing_count} rows), skipping.")
        return

    products = db.query(Product).all()
    customers = db.query(Customer).all()

    if not products:
        print("No products found. Run seed_products first.")
        return

    for _ in range(orders_count):
        # agar customer bo'lsa - random birini olamiz, bo'lmasa guest
        customer = choice(customers) if customers else None

        if customer:
            customer_name = customer.full_name
            customer_phone = customer.phone
            address = customer.default_address or fake.address().replace("\n", ", ")
            customer_id = customer.id
        else:
            customer_name = fake.name()
            customer_phone = fake.phone_number()
            address = fake.address().replace("\n", ", ")
            customer_id = None

        order = Order(
            customer_id=customer_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            address=address,
            status="new",
            total_price=0,
        )
        db.add(order)
        db.flush()

        total_price = 0
        for _ in range(randint(2, 4)):
            product = choice(products)
            quantity = randint(1, 5)
            unit_price = product.price
            line_total = unit_price * quantity

            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                unit_price=unit_price,
                quantity=quantity,
                total_price=line_total,
            )
            db.add(item)
            total_price += line_total

        order.total_price = total_price
        db.add(order)

    db.commit()
    print(f"Created {orders_count} fake orders.")


def main():
    db = SessionLocal()
    try:
        seed_customers(db)
        seed_categories(db)
        seed_products(db, products_per_category=8)
        seed_orders(db, orders_count=5)
    finally:
        db.close()


if __name__ == "__main__":
    main()
