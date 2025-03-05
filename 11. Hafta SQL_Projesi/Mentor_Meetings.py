from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QHeaderView, QLineEdit, QVBoxLayout, QTableWidgetItem, QAbstractItemView, QWidget, QHBoxLayout, QComboBox
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
    """Veritabanına bağlan ve bağlantıyı döndür."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

class MentorMeetingsWindow(QtWidgets.QWidget):

    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window  # Önceki pencereyi sakla
        self.initUi()

    def load_meetings_from_db(self, filter_status=None):
        """📌 SQL'den Mentor Görüşme Verilerini Çeker ve Tabloya Ekler"""
        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            query = "SELECT GorusmeTarihi, KursiyerID, MentorAdSoyad, BilgiSahibiMi, YogunlukDurumu, Yorumlar FROM Mentortablosu"
            params = []

            if filter_status and filter_status != "Lütfen seçiniz":
                query += " WHERE YogunlukDurumu = %s"
                params.append(filter_status)

            cursor.execute(query, params)
            data = cursor.fetchall()
            self.tableWidget.setRowCount(len(data))

            for row_idx, (gorusme_tarihi, kursiyer_id, mentor_ad, bilgi_sahibi, yogunluk, yorum) in enumerate(data):
                self.tableWidget.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(gorusme_tarihi)))
                self.tableWidget.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(kursiyer_id)))
                self.tableWidget.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(mentor_ad))
                self.tableWidget.setItem(row_idx, 3, QtWidgets.QTableWidgetItem("Evet" if bilgi_sahibi else "Hayır"))
                self.tableWidget.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(yogunluk))
                self.tableWidget.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(yorum))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def search_by_name(self):
        """📌 Kullanıcı ismine göre mentor görüşmelerini filtreler."""
        search_text = self.line_mentor_search.text().strip().lower()

        conn = get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT GorusmeTarihi, KursiyerID, MentorAdSoyad, BilgiSahibiMi, YogunlukDurumu, Yorumlar FROM Mentortablosu WHERE LOWER(MentorAdSoyad) LIKE %s", (f"%{search_text}%",))
            data = cursor.fetchall()
            self.tableWidget.setRowCount(len(data))

            for row_idx, (gorusme_tarihi, kursiyer_id, mentor_ad, bilgi_sahibi, yogunluk, yorum) in enumerate(data):
                self.tableWidget.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(gorusme_tarihi)))
                self.tableWidget.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(kursiyer_id)))
                self.tableWidget.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(mentor_ad))
                self.tableWidget.setItem(row_idx, 3, QtWidgets.QTableWidgetItem("Evet" if bilgi_sahibi else "Hayır"))
                self.tableWidget.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(yogunluk))
                self.tableWidget.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(yorum))

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"SQL hatası: {e}")

    def filter_by_status(self):
        """📌 Drop-down menüden seçilen duruma göre verileri filtreler."""
        selected_status = self.combo_mentor_dropmenu.currentText()
        self.load_meetings_from_db(filter_status=selected_status)

    def clear_table(self):
        """📌 Tabloyu temizler ve tüm verileri tekrar yükler."""
        self.tableWidget.setRowCount(0)
        self.line_mentor_search.clear()
        self.combo_mentor_dropmenu.setCurrentIndex(0)
        self.load_meetings_from_db()

    def show_comment_details(self, row, column):
        """📌 Yorumu tam olarak göstermek için tıklama olayını işler."""
        if column == 5:  # Yorumlar sütunu
            comment_text = self.tableWidget.item(row, column).text()
            QtWidgets.QMessageBox.information(self, "Tam Yorum", comment_text)

    def initUi(self):
        """📌 UI Bileşenlerini Başlatır."""
        self.setObjectName("Form")
        self.resize(700, 464)
        self.setFixedSize(700, 464)

        self.label_mentor_header = QtWidgets.QLabel(parent=self)
        self.label_mentor_header.setGeometry(QtCore.QRect(120, 40, 391, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_mentor_header.setFont(font)
        self.label_mentor_header.setText("Mentor Meetings")

        self.line_mentor_search = QtWidgets.QLineEdit(parent=self)
        self.line_mentor_search.setGeometry(QtCore.QRect(60, 110, 151, 21))
        self.line_mentor_search.returnPressed.connect(self.search_by_name)

        self.push_mentor_search = QtWidgets.QPushButton("Search", parent=self)
        self.push_mentor_search.setGeometry(QtCore.QRect(220, 110, 81, 21))
        self.push_mentor_search.clicked.connect(self.search_by_name)

        self.push_mentor_clear = QtWidgets.QPushButton("Clear", parent=self)
        self.push_mentor_clear.setGeometry(QtCore.QRect(420, 110, 81, 21))
        self.push_mentor_clear.clicked.connect(self.clear_table)

        self.push_mentor_all_meetings = QtWidgets.QPushButton("All Meetings", parent=self)
        self.push_mentor_all_meetings.setGeometry(QtCore.QRect(320, 110, 81, 21))
        self.push_mentor_all_meetings.clicked.connect(lambda: self.load_meetings_from_db())

        self.combo_mentor_dropmenu = QComboBox(parent=self)
        self.combo_mentor_dropmenu.setGeometry(QtCore.QRect(50, 150, 450, 31))
        self.combo_mentor_dropmenu.addItem("Lütfen seçiniz")
        self.combo_mentor_dropmenu.addItems(["Yoğun", "Orta", "Düşük"])  # Örnek yoğunluk durumları
        self.combo_mentor_dropmenu.currentIndexChanged.connect(self.filter_by_status)

        # self.label = QtWidgets.QLabel(parent=self)
        # self.label.setGeometry(QtCore.QRect(0, -5, 700, 471))
        # self.label.setPixmap(QtGui.QPixmap("/Users/mehmetgezer/Python Calismalari/11. Hafta SQL_Projesi/background.jpg"))
        # self.label.setScaledContents(True)

        self.tableWidget = QtWidgets.QTableWidget(parent=self)
        self.tableWidget.setGeometry(QtCore.QRect(20, 200, 620, 191))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Meeting Date", "Kursiyer ID", "Mentor", "IT Knowledge", "Intensity", "Comments"])
        self.tableWidget.cellClicked.connect(self.show_comment_details)

        self.load_meetings_from_db()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MentorMeetingsWindow()
    window.show()
    sys.exit(app.exec())
