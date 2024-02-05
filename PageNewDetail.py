from PyQt5.QtWidgets import *
import easygui
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QCursor
from PyQt5.QtCore import Qt, QPointF
from PyQt5.Qt import QFontDatabase
import DataManager
from WorkWithFiles import open_and_copypath, copyfile

AlphCodes = {502, 505, 510, 935, 241, 146, 501, 531, 552, 564, 533, 579, 564, 554, 560, 557, 405, 413, 418, 610, 611}

class PageNewDetail(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        shadow = QGraphicsDropShadowEffect(self,
                                           blurRadius=35,
                                           color=QColor(0, 0, 0, 35),
                                           offset=QPointF(10, 10),
                                           )
        self.setGraphicsEffect(shadow)
        fontId = QFontDatabase.addApplicationFont("Fonts/Circe-Regular.ttf")
        Circle_Regular = QFontDatabase.applicationFontFamilies(fontId)[0]

        self.lTitle = QLabel(self)
        self.lTitle.move(108, 27)
        self.lTitle.setFont(QFont(Circle_Regular, 25))
        self.lTitle.setStyleSheet('''color: White''')
        self.lTitle.setText("Добавление нового оборудования")
        self.lTitle.resize(1000, 50)

        self.passport = ""
        self.pashref = None
        self.imghref = None
        self.flagAboutCreateNewDetail = False
        self.lName = QLabel(self)
        self.lName.move(108, 80)
        self.lName.resize(450, 40)
        self.lName.setText("Наименование")
        self.lName.setFont(QFont(Circle_Regular, 15))
        self.inName = QLineEdit(self)
        self.inName.move(108, 114)
        self.inName.resize(450, 40)
        self.inName.setPlaceholderText("Наименование")
        self.inName.setFont(QFont(Circle_Regular, 15))

        self.lNumber = QLabel(self)
        self.lNumber.move(562, 80)
        self.lNumber.setText("Шифр")
        self.lNumber.setFont(QFont(Circle_Regular, 15))
        self.lNumber.resize(450, 40)
        self.inNumber = QLineEdit(self)
        self.inNumber.move(562, 114)
        self.inNumber.resize(450, 40)
        self.inNumber.setPlaceholderText("Шифр")
        self.inNumber.setFont(QFont(Circle_Regular, 15))

        self.lOuterDiam = QLabel(self)
        self.lOuterDiam.move(108, 228)
        self.lOuterDiam.setText("Наружный диаметр, мм")
        self.lOuterDiam.resize(450, 40)
        self.lOuterDiam.setFont(QFont(Circle_Regular, 15))
        self.inOuterDiam = QLineEdit(self)
        self.inOuterDiam.move(108, 262)
        self.inOuterDiam.resize(450, 40)
        self.inOuterDiam.setPlaceholderText("Наружный диаметр")
        self.inOuterDiam.setFont(QFont(Circle_Regular, 15))

        self.lInnerDiam = QLabel(self)
        self.lInnerDiam.move(562, 228)
        self.lInnerDiam.resize(450, 40)
        self.lInnerDiam.setText("Внутренний диаметр, мм")
        self.lInnerDiam.setFont(QFont(Circle_Regular, 15))
        self.inInnerDiam = QLineEdit(self)
        self.inInnerDiam.move(562, 262)
        self.inInnerDiam.resize(450, 40)
        self.inInnerDiam.setPlaceholderText("Внутренний диаметр")
        self.inInnerDiam.setFont(QFont(Circle_Regular, 15))

        self.lLength = QLabel(self)
        self.lLength.move(562, 154)
        self.lLength.resize(450, 40)
        self.lLength.setText("Длина, мм")
        self.lLength.setFont(QFont(Circle_Regular, 15))
        self.inLength = QLineEdit(self)
        self.inLength.move(562, 188)
        self.inLength.resize(450, 40)
        self.inLength.setPlaceholderText("Длина")
        self.inLength.setFont(QFont(Circle_Regular, 15))

        self.lMass = QLabel(self)
        self.lMass.move(108, 154)
        self.lMass.resize(450, 40)
        self.lMass.setText("Масса, кг")
        self.lMass.setFont(QFont(Circle_Regular, 15))
        self.inMass = QLineEdit(self)
        self.inMass.move(108, 188)
        self.inMass.resize(450, 40)
        self.inMass.setPlaceholderText("Масса")
        self.inMass.setFont(QFont(Circle_Regular, 15))

        self.lHref = QPushButton("Загрузить изображение", self)
        self.lHref.move(200, 336)
        self.lHref.resize(200, 40)
        self.lHref.clicked.connect(self.addHref)
        self.lHref.setFont(QFont(Circle_Regular, 15))

        self.lpassport = QPushButton("Загрузить паспорт", self)
        self.lpassport.move(670, 336)
        self.lpassport.resize(200, 40)
        self.lpassport.clicked.connect(self.addpassport)
        self.lpassport.setFont(QFont(Circle_Regular, 15))

        self.butLeft = QPushButton("Назад", self)
        self.butLeft.move(108, 447)
        self.butLeft.resize(104, 50)
        self.butLeft.setFont(QFont(Circle_Regular, 15))

        self.butCreate = QPushButton("Добавить", self)
        self.butCreate.setFont(QFont(Circle_Regular, 15))
        self.butCreate.move(888, 447)
        self.butCreate.resize(104, 50)
        self.butCreate.setStyleSheet("QPushButton {background-color: rgb(235,86,79); color: White; border-radius: 1px;}"
                                    "QPushButton:pressed {background-color:rgb(251,114,107) ; }")

        self.lHref.enterEvent = self.onCursor
        self.lHref.leaveEvent = self.offCursor
        self.lpassport.enterEvent = self.onCursor
        self.lpassport.leaveEvent = self.offCursor
        self.butLeft.enterEvent = self.onCursor
        self.butLeft.leaveEvent = self.offCursor
        self.butCreate.enterEvent = self.onCursor
        self.butCreate.leaveEvent = self.offCursor
        self.SetNormalSize()

    def clickbutCreate(self, thread_type):
        try:
            if not (self.inNumber.text()=="" or self.inName.text() == "" or self.inOuterDiam.text() == "" or
                self.inInnerDiam.text() == "" or self.inLength.text() == "" or self.inMass.text() == "" or self.pashref == None):
                if int(self.inNumber.text()[0:3]) in AlphCodes:
                    if self.imghref == None:
                        self.imghref = f"image/{self.inNumber.text()[0:3]}.png"
                    DataManager.sql_query(f"INSERT INTO Compon (code, name, thread_type, outer_diam, inner_diam, length, mass, passport, link_image) VALUES "
                          f"('{self.inNumber.text()}', '{self.inName.text()}', '{thread_type}', '{self.inOuterDiam.text()}', "
                          f"'{self.inInnerDiam.text()}', '{self.inLength.text()}', '{self.inMass.text()}', '{self.pashref}', '{self.imghref}');")
                    self.flagAboutCreateNewDetail = True
                else:
                    msg = QMessageBox.critical(self, "Ошибка ", "Неверный шифр", QMessageBox.Ok)
                    return
            else:
                msg = QMessageBox.critical(self, "Ошибка ", "Нехватает данных для добавления", QMessageBox.Ok)
                return
        except:
            msg = QMessageBox.critical(self, "Ошибка ", "Ошибка заполнения или подключения к базе данных", QMessageBox.Ok)
            return
    def addpassport(self):
        self.passport = open_and_copypath("PDF-документ")
        if self.passport is not None:
            ind = self.passport.rfind("\\")
            copyfile(self.passport, "passports")
            h = self.passport[ind+1:]
            self.pashref = "passports/"+h
            self.lpassport.setText("Паспорт загружен")

    def addHref(self):
        self.href = open_and_copypath("Изображение")
        if self.href is not None:
            ind = self.href.rfind("\\")
            h = self.href[ind+1:]
            copyfile(self.href)
            self.imghref = "image/"+h
            self.lHref.setText("Изображение загружено")

    def cleanPage(self):
        self.inName.setText('')
        self.inNumber.setText('')
        self.inOuterDiam.setText('')
        self.inInnerDiam.setText('')
        self.inLength.setText('')
        self.inMass.setText('')
        self.lHref.setText("Загрузить изображение")
        self.lpassport.setText("Загрузить паспорт")

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)  # Рисование фигур
        qp.end()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)  # Установка карандаша

        qp.setBrush(QColor(254, 254, 254))  # Установка кисти
        qp.drawRoundedRect(int(50 * self.koefW), int(75 * self.koefH), int(980 * self.koefW), int(350 * self.koefH), 10, 10)   # Рисование прямоугольника

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
