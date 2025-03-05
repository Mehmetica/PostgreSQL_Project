from PyQt6 import QtWidgets
from login_page import LoginWindow  # Login ekranı için doğru import
import psycopg2
import os
# Çalışma dizinini ayarla
os.chdir("/Users/mehmetgezer/Python Calismalari/11. Hafta SQL_Projesi")

import os
# from google.oauth2 import service_account


# Veritabanı bağlantı bilgilerini tanımla
DB_CONFIG = {
    "dbname": "CRM_Project",
    "user": "postgres",
    "password": "Besiktas01!",
    "host": "localhost",
    "port": 5432
}

def get_db_connection():
    """Veritabanına bağlan ve bağlantıyı döndür."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None


# Çalışan dosyanın bulunduğu dizini al
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

# # credentials.json dosyasını kontrol et
# if not os.path.exists(CREDENTIALS_PATH):
#     raise FileNotFoundError(f"File not found: {CREDENTIALS_PATH}")

# # Google API kimlik bilgilerini yükle
# credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)



if __name__ == "__main__":
    import sys
    # Veritabanı bağlantısını test et
    conn = get_db_connection()
    if conn:
        print("Veritabanına başarılı şekilde bağlanıldı.")
        conn.close()
    else:
        print("Veritabanı bağlantısı başarısız!")

    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())


