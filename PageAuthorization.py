from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.Qt import QFontDatabase

import DataManager
import resourses
class PageAuthorization(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.koefW, self.koefH = 1, 1
        self.id_user = ""
        fontId = QFontDatabase.addApplicationFont("Fonts/Circe-Regular.ttf")
        Circle_Regular = QFontDatabase.applicationFontFamilies(fontId)[0]
        shadow = QGraphicsDropShadowEffect(self,
                                                     blurRadius=35,
                                                     color=QColor(0, 0, 0, 35),
                                                     offset=QPointF(10, 10),
                                                     )
        self.setGraphicsEffect(shadow)

        self.lAuthorization = QLabel(self)
        self.lAuthorization.move(400, 110)
        self.lAuthorization.resize(300, 40)
        self.lAuthorization.setText("Авторизация")
        self.lAuthorization.setAlignment(Qt.AlignCenter)
        self.lAuthorization.setFont(QFont(Circle_Regular, 20))

        self.lLoginError = QLabel(self)
        self.lLoginError.move(400, 30)
        self.lLoginError.resize(300, 40)
        self.lLoginError.setText("Неверный логин или пароль")
        self.lLoginError.setAlignment(Qt.AlignCenter)
        self.lLoginError.setFont(QFont(Circle_Regular, 14))
        self.lLoginError.setStyleSheet("color: White")
        self.lLoginError.hide()

        self.inLogIn = QLineEdit(self)
        self.inLogIn.editingFinished.connect(self.LoginPressed)
        self.inLogIn.move(400, 170)
        self.inLogIn.resize(300, 60)
        self.inLogIn.setPlaceholderText("Логин")
        self.inLogIn.setFont(QFont(Circle_Regular, 14))

        self.inPass = QLineEdit(self)
        self.inPass.move(400, 250)
        self.inPass.resize(300, 60)
        self.inPass.setPlaceholderText("Пароль")
        self.inPass.setFont(QFont("Circle_Regular", 14))
        self.inPass.setEchoMode(QLineEdit.Password)

        self.butLogIn = QPushButton("Войти", self)
        self.butLogIn.setShortcut('+')
        self.butLogIn.resize(300, 60)
        self.butLogIn.move(400, 330)
        self.butLogIn.setFont(QFont("Circle_Regular", 16))
        self.butLogIn.setStyleSheet("QPushButton {background-color: rgb(235,86,79); color: White; border-radius: 1px;}"
                           "QPushButton:pressed {background-color:rgb(251,114,107) ; }")

        self.butLogIn.enterEvent = self.onCursor
        self.butLogIn.leaveEvent = self.offCursor
        self.SetNormalSize()

    def LoginPressed(self):
        self.inPass.setFocus()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor("#d4d4d4")
        qp.setPen(col)
        qp.setBrush(QColor(254, 254, 254))
        qp.drawRoundedRect(int(375 * self.koefW), int(75 * self.koefH), int(350 * self.koefW), int(350 * self.koefH), 10, 10)   # Рисование прямоугольника

    def LogIn(self):
        login = self.inLogIn.text()
        password = self.inPass.text()
        id = DataManager.select_users_where("id", f"login='{login}' AND password='{password}'")
        if id:
            id_user = id[0][0]
            self.lLoginError.hide()
            return id_user
        else:
            self.lLoginError.show()
            return False

    def LogOut(self):
        self.inPass.clear()
        self.inLogIn.clear()


    def onCursor(self, e):
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def offCursor(self, e):
        self.setCursor(QCursor(Qt.ArrowCursor))


    def SetNormalSize(self):
        for i in self.children():
            try:
                i.x0 = i.x()
                i.y0 = i.y()
                i.width0 = i.width()
                i.height0 = i.height()
            except:
                pass
    def DynamicSize(self, koefW, koefH):
        for i in self.children():
            try:
                i.resize(int(i.width0 * koefW), int(i.height0 * koefH))
                i.move(int(i.x0 * koefW), int(i.y0 * koefH))
                self.koefW = koefW
                self.koefH = koefH

            except:
                pass