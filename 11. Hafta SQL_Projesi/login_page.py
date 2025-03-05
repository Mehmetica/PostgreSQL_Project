from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt  # Alignment için doğru modül
import psycopg2
import sys
from admin_menu_preferences import AdminMenuPreferencesWindow
from user_menu import UserMenuWindow

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

class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setFixedSize(400, 300)  # Pencere boyutunu sabitler

        # Arka plan resmi ayarı
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setPixmap(QtGui.QPixmap("/Users/mehmetgezer/Python Calismalari/11. Hafta SQL_Projesi/login.jpg"))

        # Başlık
        self.label_title = QtWidgets.QLabel(Form)
        self.label_title.setGeometry(50, 20, 300, 50)
        self.label_title.setText("CRM PROJECT")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")

        # Username etiketi
        self.label_username = QtWidgets.QLabel(Form)
        self.label_username.setGeometry(50, 100, 100, 30)
        self.label_username.setText("Username:")
        self.label_username.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")

        # Username giriş kutusu
        self.line_login_username = QtWidgets.QLineEdit(Form)
        self.line_login_username.setGeometry(150, 100, 200, 30)
        self.line_login_username.setStyleSheet(
            "background-color: #FFFFFF; border: 1px solid #000000; border-radius: 5px; color:black; "
        )

        # Password etiketi
        self.label_password = QtWidgets.QLabel(Form)
        self.label_password.setGeometry(50, 150, 100, 30)
        self.label_password.setText("Password:")
        self.label_password.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")

        # Password giriş kutusu
        self.line_login_password = QtWidgets.QLineEdit(Form)
        self.line_login_password.setGeometry(150, 150, 200, 30)
        self.line_login_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.line_login_password.setStyleSheet(
            "background-color: #FFFFFF; border: 1px solid #000000; border-radius: 5px; color:black;"
        )

        # Login butonu
        self.push_login_login = QtWidgets.QPushButton(Form)
        self.push_login_login.setGeometry(100, 220, 100, 30)
        self.push_login_login.setText("Login")
        self.push_login_login.setStyleSheet(
            "background-color: #FFC107; color: black; font-weight: bold; border-radius: 5px;"
        )

        # Exit butonu
        self.push_login_exit = QtWidgets.QPushButton(Form)
        self.push_login_exit.setGeometry(210, 220, 100, 30)
        self.push_login_exit.setText("Exit")
        self.push_login_exit.setStyleSheet(
            "background-color: #FFC107; color: black; font-weight: bold; border-radius: 5px;"
        )

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.push_login_login.clicked.connect(self.validate_login)
        self.ui.push_login_exit.clicked.connect(self.close_application)

    def validate_login(self):
        """📌 Kullanıcı adı ve şifreyi SQL veritabanından kontrol eder."""
        username = self.ui.line_login_username.text()
        password = self.ui.line_login_password.text()

        conn = get_db_connection()
        if not conn:
            QtWidgets.QMessageBox.warning(self, "Veritabanı Hatası", "Veritabanına bağlanılamadı!")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT yetki FROM Kullanicilar WHERE kullaniciadi = %s AND parola = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:  # Eğer kullanıcı bulunduysa
                yetki = user[0]  # Kullanıcının yetkisini al
                if yetki == 'admin':
                    self.open_admin_menu()
                elif yetki == 'user':
                    self.open_user_menu()
                else:
                    QtWidgets.QMessageBox.warning(self, "Giriş Başarısız", "Bilinmeyen rol algılandı.")
            else:
                QtWidgets.QMessageBox.warning(self, "Giriş Başarısız", "Geçersiz kullanıcı adı veya şifre!")

        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "SQL Hatası", f"Bir hata oluştu: {e}")

    def open_admin_menu(self):
        """📌 Başarılı giriş sonrası Admin Menü ekranını açar."""
        self.admin_menu = AdminMenuPreferencesWindow()
        self.admin_menu.show()
        self.close()

    def open_user_menu(self):
        """📌 Başarılı giriş sonrası Kullanıcı Menü ekranını açar."""
        self.user_menu = UserMenuWindow()
        self.user_menu.show()
        self.close()

    def close_application(self):
        """📌 Uygulamayı kapatır."""
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
