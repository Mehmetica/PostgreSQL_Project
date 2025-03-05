from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
import sys
import smtplib
from email.mime.text import MIMEText

# PostgreSQL Veritabanı Bağlantı Bilgileri
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

class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(682, 411)
        Form.setFixedSize(682, 411)

        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(-20, -10, 711, 431))
        self.label.setPixmap(QtGui.QPixmap("/Users/mehmetgezer/Python Calismalari/Bitirme_Projesi/background.jpg"))
        self.label.setScaledContents(True)

        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(20, 140, 641, 221))
        self.frame.setStyleSheet("QFrame { background-color: #F0F0F0; border: 2px solid black; border-radius: 10px; }")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_admin_header = QtWidgets.QLabel(parent=Form)
        self.label_admin_header.setGeometry(QtCore.QRect(150, 30, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        self.label_admin_header.setFont(font)
        self.label_admin_header.setStyleSheet("background-color: rgb(223, 194, 107); color: rgb(2, 50, 90); border-radius: 10px; padding: 5px;")
        self.label_admin_header.setText("               Admin Menu")

        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.frame)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 20, 621, 191))
        self.tableWidget_2.setStyleSheet("QTableWidget { background-color: rgb(240, 240, 240); gridline-color: #D5D8DC; border: 1px solid #BDC3C7; color: black; }")
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["ID", "Ad Soyad", "Mail Adresi", "Telefon No", "Eyalet"])
        self.tableWidget_2.horizontalHeader().setStyleSheet("color: black;")
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget_2.verticalHeader().setStyleSheet("color: black;")

        self.push_admin_students = QtWidgets.QPushButton(parent=Form)
        self.push_admin_students.setGeometry(QtCore.QRect(60, 100, 151, 31))
        self.push_admin_students.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.push_admin_students.setText("Show All Students")
        
        self.push_admin_mail = QtWidgets.QPushButton(parent=Form)
        self.push_admin_mail.setGeometry(QtCore.QRect(270, 100, 151, 31))
        self.push_admin_mail.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.push_admin_mail.setText("Mail")
        
        self.push_admin_menu = QtWidgets.QPushButton(parent=Form)
        self.push_admin_menu.setGeometry(QtCore.QRect(470, 100, 151, 31))
        self.push_admin_menu.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.push_admin_menu.setText("Main Menu")
        
        self.push_admin_exit = QtWidgets.QPushButton(parent=Form)
        self.push_admin_exit.setGeometry(QtCore.QRect(10, 370, 75, 24))
        self.push_admin_exit.setStyleSheet("QPushButton { background-color: rgb(209, 0, 0); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.push_admin_exit.setText("Exit")

class AdminMenuWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.push_admin_students.clicked.connect(self.load_students_data)
        self.push_admin_mail.clicked.connect(self.send_mail)
        self.push_admin_menu.clicked.connect(self.close)
        self.push_admin_exit.clicked.connect(self.close)
    
    def load_students_data(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT kursiyerid, adsoyad, mailadresi, telefonnumarasi, yasadiginizeyalet FROM kursiyerler")
                students = cursor.fetchall()
                
                self.tableWidget_2.setRowCount(len(students))
                for row_idx, row_data in enumerate(students):
                    for col_idx, cell_data in enumerate(row_data):
                        self.tableWidget_2.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell_data)))
                
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Veri çekme hatası: {e}")
        else:
            print("Veritabanına bağlanılamadı.")



    def send_mail(self):
        sender_email = "mehmetica74@gmail.com"
        sender_password = "Haticemehmet2015!"
        subject = "Selam"
        body = "Selam"

        selected_row = self.tableWidget_2.currentRow()
        if selected_row == -1:
            print("Lütfen bir öğrenci seçin.")
            return

        recipient_email = self.tableWidget_2.item(selected_row, 2).text()
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print("Mail gönderildi.")
        except Exception as e:
            print(f"Mail gönderme hatası: {e}")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    admin_menu = AdminMenuWindow()
    admin_menu.show()
    sys.exit(app.exec())