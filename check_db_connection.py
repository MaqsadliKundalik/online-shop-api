import psycopg2
import sys

# Konfiguratsiyadan olingan ma'lumotlar
DB_NAME = "tbozozuz_bozor"
DB_USER = "tbozozuz_bozorchi"
DB_PASS = "oddiyparol123"
DB_PORT = "5432"

def test_connection(host):
    print(f"--------------------------------------------------")
    print(f"[{host}] ga ulanishga harakat qilinmoqda...")
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=host,
            port=DB_PORT,
            connect_timeout=10
        )
        print(f"MUVAFFAQIYAT: {host} ga ulanish o'rnatildi!")
        
        # Versiyani tekshirish
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        print(f"PostgreSQL versiyasi: {version}")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"XATOLIK: {host} ga ulanib bo'lmadi.")
        print(f"Xato matni: {e}")
        return False

if __name__ == "__main__":
    print("Ma'lumotlar bazasiga ulanishni tekshirish skripti")
    print(f"Baza: {DB_NAME}, Foydalanuvchi: {DB_USER}")
    
    # 1. Localhost orqali
    success_localhost = test_connection("localhost")
    
    # 2. 127.0.0.1 orqali (ba'zan localhost ishlamasligi mumkin)
    print("\n")
    success_ip = test_connection("127.0.0.1")
    
    if success_localhost or success_ip:
        print("\n--------------------------------------------------")
        print("XULOSA: Baza bilan aloqa mavjud! ")
        print("Agar loyiha hali ham ishlamayotgan bo'lsa, 'app/core/config.py' faylidagi o'zgarishlar serverga yuklanganligini tekshiring.")
    else:
        print("\n--------------------------------------------------")
        print("XULOSA: Baza bilan aloqa YO'Q.")
        print("Iltimos, cPanelda baza nomi, foydalanuvchi va parol to'g'riligini tekshiring.")
        print("Shuningdek, foydalanuvchi bazaga biriktirilganligiga (Add User to Database) ishonch hosil qiling.")
