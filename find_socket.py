import os
import psycopg2
import sys

# Konfiguratsiya
DB_NAME = "tbozozuz_bozor"
DB_USER = "tbozozuz_bozorchi"
DB_PASS = "oddiyparol123"
DB_PORT = "5432"

COMMON_SOCKET_PATHS = [
    "/tmp",
    "/var/run/postgresql",
    "/var/lib/postgresql",
    "/run/postgresql",
    "/var/pgsql_socket",
    "/var/run"
]

def try_connect(host_path):
    print(f"[{host_path}] orqali ulanish...")
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=host_path,
            port=DB_PORT,
            connect_timeout=5
        )
        print(f"  >>> MUVAFFAQIYAT! Soket topildi va ishlovchi manzil: {host_path}")
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"  - Ulana olmadi: {e}")
        return False
    except Exception as e:
        print(f"  - Boshqa xato: {e}")
        return False

def find_sockets():
    print("Soket fayllarni qidirish...")
    found_sockets = []
    for base_dir in COMMON_SOCKET_PATHS:
        if os.path.exists(base_dir):
            if os.access(base_dir, os.R_OK):
                try:
                    files = os.listdir(base_dir)
                    for f in files:
                        if f.startswith(".s.PGSQL") and not f.endswith(".lock"):
                            full_path = base_dir
                            print(f"  Soket fayl topildi: {os.path.join(base_dir, f)}")
                            found_sockets.append(base_dir)
                except Exception as e:
                    print(f"  {base_dir} ni o'qib bo'lmadi: {e}")
            else:
                print(f"  {base_dir} ga ruxsat yo'q.")
        else:
            # print(f"  {base_dir} mavjud emas.")
            pass
    return list(set(found_sockets))

if __name__ == "__main__":
    print("--- PostgreSQL Soket Qidiruvchisi ---")
    
    # 1. Tizimdagi fayllarni qidirish
    candidates = find_sockets()
    
    success = False
    
    # 2. Topilgan yo'llarni sinab ko'rish
    if candidates:
        print("\nTopilgan soketlar orqali ulanib ko'ramiz:")
        for path in candidates:
            if try_connect(path):
                success = True
                print(f"\nTAKLIF: `app/core/config.py` faylida mana bu manzilni ishlating:")
                print(f'DATABASE_URL = "postgresql://{DB_USER}:{DB_PASS}@{path}/{DB_NAME}"')
                break
    else:
        print("\nAvtomatik qidiruv natija bermadi.")

    # 3. Agar topilmasa, hostni bo'sh qoldirib ko'rish (libhq kutubxonasi o'zi qidirsin)
    if not success:
        print("\nStandart (bo'sh host) orqali ulanib ko'ramiz...")
        if try_connect(""): # bo'sh string default lokatsiyalarni tekshiradi
            success = True
            print(f"\nTAKLIF: `app/core/config.py` faylida hostni ko'rsatmang:")
            print(f'DATABASE_URL = "postgresql://{DB_USER}:{DB_PASS}@/{DB_NAME}"')

    if not success:
        print("\n------------------------------------------------")
        print("XULOSA: Soket topilmadi va TCP bloklangan.")
        print("Iltimos, hosting provayderidan (Ahost) 'PostgreSQL socket path' qayerda ekanligini so'rang.")
