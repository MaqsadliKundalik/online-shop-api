# app/admin/views.py
from sqladmin import ModelView

from app.models.user import AdminUser
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.customer import Customer
from uuid import uuid4
from pathlib import Path

from wtforms import FileField
from sqladmin import ModelView

from app.models.product import Product


class ProductAdmin(ModelView, model=Product):
    name = "Product"
    name_plural = "Products"
    icon = "fa-solid fa-box"

    # Jadvalda ko'rinadigan ustunlar
    column_list = [
        Product.id,
        Product.name,
        Product.price,
        Product.status,
        Product.is_top,
        Product.category,
        Product.image_path,  # agar shunaqa ustun bo'lsa
    ]
    column_searchable_list = [Product.name]
    column_sortable_list = [Product.id, Product.price]

    # Formda qaysi ustunlar chiqishi
    form_columns = [
        "name",
        "price",
        "description",
        "status",
        "is_top",
        "category",
        "image_path",  # bu uchun file input qo'yamiz
    ]

    # image_path ustunini FileField qilib beramiz
    form_overrides = {
        "image_path": FileField,
    }

    async def on_model_change(self, form, model, is_created):
        """
        Form submit bo'lganda faylni diskka saqlab, model.image_path ga nomini yozamiz.
        """
        file = form.image_path.data  # bu UploadFile emas, werkzeug FileStorage bo'ladi

        if file:
            ext = file.filename.split(".")[-1]
            filename = f"{uuid4()}.{ext}"

            upload_dir = Path("static") / "images"
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_path = upload_dir / filename

            # faylni saqlash
            with file_path.open("wb") as f:
                f.write(file.read())

            # model ustuniga faqat relative path/filename saqlaymiz
            model.image_path = f"images/{filename}"
        else:
            # agar formda fayl yuborilmagan bo'lsa va eski record bo'lsa,
            # mavjud image_path ni o'zgartirmaymiz
            if not is_created:
                pass

class CustomerAdmin(ModelView, model=Customer):
    name = "Customer"
    name_plural = "Customers"
    icon = "fa-solid fa-user"

    column_list = [
        Customer.id,
        Customer.full_name,
        Customer.phone,
        Customer.default_address,
        Customer.created_at,
    ]
    column_searchable_list = [Customer.full_name, Customer.phone]
    column_sortable_list = [Customer.id, Customer.created_at]

class AdminUserAdmin(ModelView, model=AdminUser):
    name = "Admin"
    name_plural = "Admins"
    icon = "fa-solid fa-user"

    column_list = [AdminUser.id, AdminUser.username, AdminUser.is_superuser]
    column_searchable_list = [AdminUser.username]
    column_sortable_list = [AdminUser.id, AdminUser.username]

    form_excluded_columns = []


class CategoryAdmin(ModelView, model=Category):
    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-tags"

    column_list = "__all__"
    column_searchable_list = [Category.name]


class OrderAdmin(ModelView, model=Order):
    name = "Order"
    name_plural = "Orders"
    icon = "fa-solid fa-shopping-cart"

    column_list = [
        Order.id,
        Order.customer_name,
        Order.customer_phone,
        Order.status,
        Order.total_price,
        Order.created_at,
    ]
    column_searchable_list = [Order.customer_name, Order.customer_phone, Order.status]
    column_sortable_list = [Order.id, Order.created_at, Order.total_price]


class OrderItemAdmin(ModelView, model=OrderItem):
    name = "Order Item"
    name_plural = "Order Items"
    icon = "fa-solid fa-list"

    column_list = "__all__"
