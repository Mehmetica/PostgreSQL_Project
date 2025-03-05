from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
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

class InterviewsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        """📌 UI Bileşenlerini Başlatır."""
        self.setObjectName("Form")
        self.resize(681, 481)
        self.setMinimumSize(QtCore.QSize(681, 481))

        self.label_2 = QtWidgets.QLabel(parent=self)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 391, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_2.setFont(font)
        self.label_2.setText("Interviews")

        self.lineEdit_search = QtWidgets.QLineEdit(parent=self)
        self.lineEdit_search.setGeometry(QtCore.QRect(240, 80, 271, 21))
        self.lineEdit_search.setPlaceholderText("Enter text to search...")
        self.lineEdit_search.returnPressed.connect(self.search_user)

        self.pushButton_search = QtWidgets.QPushButton("Search", parent=self)
        self.pushButton_search.setGeometry(QtCore.QRect(100, 80, 121, 21))
        self.pushButton_search.clicked.connect(self.search_user)

        self.pushButton_exit = QtWidgets.QPushButton("Exit", parent=self)
        self.pushButton_exit.setGeometry(QtCore.QRect(590, 430, 75, 24))
        self.pushButton_exit.clicked.connect(self.close)

        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self)
        self.tableWidget_2.setGeometry(QtCore.QRect(50, 140, 601, 271))
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(["Fullname", "Project Submission Date", "Project Development Date"])
        
        self.pushButton_submitted = QtWidgets.QPushButton("Projects Submitted", parent=self)
        self.pushButton_submitted.setGeometry(QtCore.QRect(110, 105, 131, 31))
        self.pushButton_submitted.clicked.connect(self.show_submitted_projects)

        self.pushButton_received = QtWidgets.QPushButton("Projects Received", parent=self)
        self.pushButton_received.setGeometry(QtCore.QRect(280, 105, 131, 31))
        self.pushButton_received.clicked.connect(self.show_received_projects)

        self.pushButton_main_menu = QtWidgets.QPushButton("Main Menu", parent=self)
        self.pushButton_main_menu.setGeometry(QtCore.QRect(450, 105, 131, 31))
        self.pushButton_main_menu.clicked.connect(self.close)

        # Başlangıçta tüm verileri yükle
        self.load_all_data()

    def load_all_data(self):
        """📌 `projetakiptablosu` tablosundan tüm projeleri yükler."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT k.AdSoyad, p.ProjeGonderilisTarihi, p.ProjeninGelisTarihi 
                FROM projetakiptablosu p
                JOIN kursiyerler k ON p.KursiyerID = k.KursiyerID
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def search_user(self):
        """📌 Kullanıcı adına göre `projetakiptablosu` tablosunu filtreler."""
        search_text = self.lineEdit_search.text().strip().lower()

        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT k.AdSoyad, p.ProjeGonderilisTarihi, p.ProjeninGelisTarihi 
                FROM projetakiptablosu p
                JOIN kursiyerler k ON p.KursiyerID = k.KursiyerID
                WHERE LOWER(k.AdSoyad) LIKE %s
            """
            cursor.execute(query, (f"%{search_text}%",))
            data = cursor.fetchall()
            self.populate_table(data)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def show_submitted_projects(self):
        """📌 Gönderilmiş projeleri göster (`ProjeGonderilisTarihi` dolu olanlar)."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT k.AdSoyad, p.ProjeGonderilisTarihi 
                FROM projetakiptablosu p
                JOIN kursiyerler k ON p.KursiyerID = k.KursiyerID
                WHERE p.ProjeGonderilisTarihi IS NOT NULL
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data, columns=2)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def show_received_projects(self):
        """📌 Geliş tarihi belli olan projeleri göster (`ProjeninGelisTarihi` dolu olanlar)."""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = """
                SELECT k.AdSoyad, p.ProjeninGelisTarihi 
                FROM projetakiptablosu p
                JOIN kursiyerler k ON p.KursiyerID = k.KursiyerID
                WHERE p.ProjeninGelisTarihi IS NOT NULL
            """
            cursor.execute(query)
            data = cursor.fetchall()
            self.populate_table(data, columns=2)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def populate_table(self, data, columns=3):
        """📌 Verileri tabloya ekler."""
        self.tableWidget_2.setRowCount(len(data))
        self.tableWidget_2.setColumnCount(columns)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.tableWidget_2.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InterviewsWindow()
    window.show()
    sys.exit(app.exec())
