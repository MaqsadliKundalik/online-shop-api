from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.models.user import AdminUser

# Jadval bo'lmasa yaratib qo'yamiz (ishonch uchun)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

username = "admin"
password = "admin123"  # BU YERGA XOHLAGAN PAROLINGNI YOZ

user = db.query(AdminUser).filter_by(username=username).first()

if user:
    print(f"Existing admin topildi: {user.username}, paroli yangilanadi...")
    user.set_password(password)
else:
    print(f"Yangi admin yaratiladi: {username}")
    user = AdminUser(username=username, is_superuser=True)
    user.set_password(password)
    db.add(user)

db.commit()
db.close()
print("Done.")
