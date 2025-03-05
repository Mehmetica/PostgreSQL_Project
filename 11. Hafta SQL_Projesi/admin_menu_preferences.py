from PyQt6 import QtCore, QtGui, QtWidgets
from Applications import ApplicationsWindow 
from Interviews import InterviewsWindow  
from Mentor_Meetings import MentorMeetingsWindow  
from Admin_Menu import AdminMenuWindow


import sys
sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(f"Error: {value}")
sys.excepthook = exception_hook



class AdminMenuPreferencesWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Pencere başlığını ve boyutlarını ayarla
        self.setObjectName("Admin_Menu_Preferences")
        self.resize(600, 400)
        self.setFixedSize(600, 400)

        # Arka plan ekleme
        self.label = QtWidgets.QLabel(parent=self)
        self.label.setGeometry(QtCore.QRect(0, -5, 601, 451))
        self.label.setPixmap(QtGui.QPixmap("/Users/mehmetgezer/Python Calismalari/Bitirme_Projesi/background.jpg"))
        self.label.setScaledContents(True)

        # Çerçeve (frame) ekleme
        self.frame = QtWidgets.QFrame(parent=self)
        self.frame.setGeometry(QtCore.QRect(80, 100, 441, 241))
        self.frame.setStyleSheet("QFrame { background-color: rgb(239, 238, 236); border: 2px solid black; border-radius: 10px; }")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # Butonlar
        self.p_Applications = QtWidgets.QPushButton(parent=self.frame)
        self.p_Applications.setGeometry(QtCore.QRect(120, 40, 211, 41))
        self.p_Applications.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.p_Applications.setText("Applications")
        self.p_Applications.clicked.connect(self.open_applications)

        self.p_mentorMeeting = QtWidgets.QPushButton(parent=self.frame)
        self.p_mentorMeeting.setGeometry(QtCore.QRect(120, 90, 211, 41))
        self.p_mentorMeeting.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.p_mentorMeeting.setText("Interviews")
        self.p_mentorMeeting.clicked.connect(self.open_interviews)

        self.p_mentorMeeting_2 = QtWidgets.QPushButton(parent=self.frame)
        self.p_mentorMeeting_2.setGeometry(QtCore.QRect(120, 140, 211, 41))
        self.p_mentorMeeting_2.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.p_mentorMeeting_2.setText("Mentor Meeting")
        self.p_mentorMeeting_2.clicked.connect(self.open_mentor_meeting)

        self.p_admin_menu = QtWidgets.QPushButton(parent=self.frame)
        self.p_admin_menu.setGeometry(QtCore.QRect(120, 190, 211, 41))
        self.p_admin_menu.setStyleSheet("QPushButton { background-color: rgb(2, 50, 90); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.p_admin_menu.setText("Admin Menu")
        self.p_admin_menu.clicked.connect(self.open_admin_menu)


        self.pushButton_exit = QtWidgets.QPushButton(parent=self)
        self.pushButton_exit.setGeometry(QtCore.QRect(240, 350, 131, 31))
        self.pushButton_exit.setStyleSheet("QPushButton { background-color: rgb(211, 0, 0); color: white; border-radius: 10px; border: 2px solid #000000; } QPushButton:hover { background-color: rgb(223, 194, 107); }")
        self.pushButton_exit.setText("Exit")
        self.pushButton_exit.clicked.connect(self.exit_program)  
        # self.pushButton_exit.clicked.connect(self.open_loginpage)


       

        # Başlık etiketi
        self.label_title = QtWidgets.QLabel(parent=self)
        self.label_title.setGeometry(QtCore.QRect(130, 80, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Onyx")
        font.setPointSize(28)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("background-color: rgb(223, 194, 107); color: rgb(2, 50, 90); border-radius: 10px; padding: 5px;")
        self.label_title.setText("             Admin Menu")
        

    def open_applications(self):
        self.applications_window = ApplicationsWindow()
        self.applications_window.show()

    def open_interviews(self):
        self.interviews_window = InterviewsWindow()
        self.interviews_window.show()

    def open_mentor_meeting(self):
        self.mentor_meetings_window = MentorMeetingsWindow()
        self.mentor_meetings_window.show()

    def open_admin_menu(self):
        self.admin_menu_window= AdminMenuWindow()
        self.admin_menu_window.show()

    # def open_loginpage(self):
    #     self.login_page= LoginWindow()
    #     self.login_page.show()

    def exit_program(self):
        from login_page import LoginWindow
        self.close()
        self.login_window= LoginWindow()
        self.login_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AdminMenuPreferencesWindow()
    window.show()
    sys.exit(app.exec())
