from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
import psycopg2
import sys

# 📌 PostgreSQL Veritabanı Bağlantı Bilgileri
DB_CONFIG = {
    "dbname": "CRM_Project",
    "user": "postgres",
    "password": "Besiktas01!",
    "host": "localhost",
    "port": 5432
}

def get_db_connection():
    """📌 Veritabanına bağlan ve bağlantıyı döndür."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

class ApplicationsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.load_all_applications()

    def setupUi(self):
        """📌 UI Bileşenlerini Başlatır."""
        self.setObjectName("Applications")
        self.resize(900, 600)

        # Arka plan etiketi
        self.label = QtWidgets.QLabel(self)
        self.label.setScaledContents(True)

        # Arama çubuğu
        self.line_app_search = QtWidgets.QLineEdit(self)
        self.line_app_search.setPlaceholderText("Enter text to search...")

        # Butonlar
        self.push_app_search = QtWidgets.QPushButton("Search", self)
        self.push_app_search.clicked.connect(self.search_user)

        self.push_load_all = QtWidgets.QPushButton("Load All Applications", self)
        self.push_load_all.clicked.connect(self.load_all_applications)

        self.push_app_unscheduled = QtWidgets.QPushButton("Unscheduled Meetings", self)
        self.push_app_unscheduled.clicked.connect(self.show_unscheduled_meetings)

        self.push_app_planned = QtWidgets.QPushButton("Planned Meetings", self)
        self.push_app_planned.clicked.connect(self.show_planned_meetings)

        self.push_app_duplicate = QtWidgets.QPushButton("Find Duplicates", self)
        self.push_app_duplicate.clicked.connect(self.find_duplicate_records)

        self.push_app_filtering = QtWidgets.QPushButton("Filter 'Status' Applications", self)
        self.push_app_filtering.clicked.connect(self.filter_applications)

        self.pushButton_exit = QtWidgets.QPushButton("Exit", self)
        self.pushButton_exit.clicked.connect(self.close)

        # Tablo
        self.table_app_anatablo = QtWidgets.QTableWidget(self)
        self.table_app_anatablo.setColumnCount(8)
        self.table_app_anatablo.setHorizontalHeaderLabels([
            "Date", "Name Surname", "Mail", "Telephone",
            "Post Code", "State", "Status", "Economic Status"
        ])
        
        # Layout düzeni
        self.layout = QtWidgets.QGridLayout()
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.layout)

        self.layout.addWidget(self.line_app_search, 0, 1, 1, 2)
        self.layout.addWidget(self.push_app_search, 0, 3)
        self.layout.addWidget(self.push_load_all, 0, 4)
        self.layout.addWidget(self.push_app_unscheduled, 0, 5)
        self.layout.addWidget(self.push_app_planned, 0, 6)
        self.layout.addWidget(self.push_app_duplicate, 1, 1)
        self.layout.addWidget(self.push_app_filtering, 1, 2)
        self.layout.addWidget(self.pushButton_exit, 1, 6)
        self.layout.addWidget(self.table_app_anatablo, 2, 1, 7, 6)

    def load_all_applications(self):
        """📌 `basvurular` tablosundaki tüm başvuruları yükler."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT b.zamandamgasi, k.AdSoyad, k.MailAdresi, k.TelefonNumarasi, 
                       k.PostaKodu, k.YasadiginizEyalet, b.suankidurum, b.ekonomikdurum
                FROM basvurular b
                JOIN kursiyerler k ON b.kursiyerid = k.kursiyerid
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def filter_applications(self):
        """📌 Başvuruları belirli bir kritere göre filtreler (Örnek: Durumu 'Beklemede' olanları gösterir)."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT b.zamandamgasi, k.AdSoyad, k.MailAdresi, k.TelefonNumarasi, 
                    k.PostaKodu, k.YasadiginizEyalet, b.suankidurum, b.ekonomikdurum
                FROM basvurular b
                JOIN kursiyerler k ON b.kursiyerid = k.kursiyerid
                WHERE b.suankidurum = 'Beklemede'  -- Burada kriteri değiştirebilirsin
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")



    def find_duplicate_records(self):
        """📌 Mükerrer (duplicate) başvuru kayıtlarını bulur."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT b.zamandamgasi, k.AdSoyad, k.MailAdresi, k.TelefonNumarasi, 
                    k.PostaKodu, k.YasadiginizEyalet, b.suankidurum, b.ekonomikdurum
                FROM basvurular b
                JOIN kursiyerler k ON b.kursiyerid = k.kursiyerid
                WHERE k.MailAdresi IN (
                    SELECT MailAdresi FROM kursiyerler GROUP BY MailAdresi HAVING COUNT(*) > 1
                )
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")
        

    def search_user(self):
        """📌 Kullanıcı adına göre `basvurular` tablosunu filtreler."""
        search_text = self.line_app_search.text().strip().lower()

        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT b.zamandamgasi, k.AdSoyad, k.MailAdresi, k.TelefonNumarasi, 
                       k.PostaKodu, k.YasadiginizEyalet, b.suankidurum, b.ekonomikdurum
                FROM basvurular b
                JOIN kursiyerler k ON b.kursiyerid = k.kursiyerid
                WHERE LOWER(k.AdSoyad) LIKE %s
            """
            cursor.execute(query, (f"%{search_text}%",))
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def show_unscheduled_meetings(self):
        """📌 Atanmamış görüşmeleri (`suankidurum = 'Beklemede'`) gösterir."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT b.zamandamgasi, k.AdSoyad, k.MailAdresi, k.TelefonNumarasi, 
                       k.PostaKodu, k.YasadiginizEyalet, b.suankidurum, b.ekonomikdurum
                FROM basvurular b
                JOIN kursiyerler k ON b.kursiyerid = k.kursiyerid
                WHERE b.suankidurum = 'Beklemede'
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def show_planned_meetings(self):
        """📌 Planlanmış görüşmeleri (`suankidurum = 'Onaylandı'`) gösterir."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT b.zamandamgasi, k.AdSoyad, k.MailAdresi, k.TelefonNumarasi, 
                       k.PostaKodu, k.YasadiginizEyalet, b.suankidurum, b.ekonomikdurum
                FROM basvurular b
                JOIN kursiyerler k ON b.kursiyerid = k.kursiyerid
                WHERE b.suankidurum = 'Onaylandı'
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def populate_table(self, data):
        """📌 Verileri tabloya ekler."""
        self.table_app_anatablo.setRowCount(len(data))
        self.table_app_anatablo.setColumnCount(8)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table_app_anatablo.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationsWindow()
    window.show()
    sys.exit(app.exec())
