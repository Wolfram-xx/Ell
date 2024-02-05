"""from datetime import datetime
from PyQt5.QtWidgets import *"""
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QCursor
from PyQt5.Qt import QFontDatabase
import resourses
import DataManager


class PageInput1(QWidget):
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
        self.lTitle.setText("Создание нового проекта")
        self.lTitle.resize(1000, 50)

        self.lCompany = QLabel(self)
        self.lCompany.move(108, 75)
        self.lCompany.setText('Компания')
        self.lCompany.setFont(QFont(Circle_Regular, 15))
        self.lCompany.setStyleSheet('''color: White''')
        self.lCompany.resize(430, 50)
        self.inCompany = QLineEdit(self)
        self.inCompany.move(108, 114)
        self.inCompany.resize(430, 50)
        self.inCompany.setPlaceholderText('Компания')
        self.inCompany.setFont(QFont(Circle_Regular, 15))

        self.lField = QLabel(self)
        self.lField.move(562, 75)
        self.lField.resize(430, 50)
        self.lField.setText('Месторождение')
        self.lField.setFont(QFont(Circle_Regular, 15))
        self.lField.setStyleSheet('''color: White''')
        self.inField = QLineEdit(self)
        self.inField.move(562, 114)
        self.inField.resize(430, 50)
        self.inField.setPlaceholderText('Месторождение')
        self.inField.setFont(QFont(Circle_Regular, 15))

        self.lWell = QLabel(self)
        self.lWell.move(108, 185)
        self.lWell.setText('Скважина')
        self.lWell.setFont(QFont(Circle_Regular, 15))
        self.lWell.setStyleSheet('''color: White''')
        self.lWell.resize(430, 50)
        self.inWell = QLineEdit(self)
        self.inWell.move(108, 225)
        self.inWell.resize(430, 50)
        self.inWell.setPlaceholderText('Скважина')
        self.inWell.setFont(QFont(Circle_Regular, 15))

        self.lBush = QLabel(self)
        self.lBush.move(562, 185)
        self.lBush.setText('Куст')
        self.lBush.setFont(QFont(Circle_Regular, 15))
        self.lBush.setStyleSheet('''color: White''')
        self.lBush.resize(430, 50)
        self.inBush = QLineEdit(self)
        self.inBush.move(562, 225)
        self.inBush.resize(430, 50)
        self.inBush.setPlaceholderText('Куст')
        self.inBush.setFont(QFont(Circle_Regular, 15))

        self.lDate = QLabel(self)
        self.lDate.move(108, 295)
        self.lDate.setText('Дата подбора')
        self.lDate.resize(275, 50)
        self.lDate.setFont(QFont(Circle_Regular, 15))
        self.lDate.setStyleSheet('''color: White''')
        self.inData = QDateEdit(self)
        self.inData.setDate(datetime.now())
        self.inData.setCalendarPopup(True)
        self.inData.move(108, 336)
        self.inData.resize(275, 50)
        self.inData.setFont(QFont(Circle_Regular, 15))

        self.lEngineer = QLabel(self)
        self.lEngineer.move(413, 295)
        self.lEngineer.resize(275, 50)
        self.lEngineer.setText('Инженер по подбору')
        self.lEngineer.setFont(QFont(Circle_Regular, 15))
        self.lEngineer.setStyleSheet('''color: White''')
        self.lEngineer.resize(275, 50)
        self.engineer_combo = QComboBox(self)
        self.engineer_combo.setFont(QFont(Circle_Regular, 15))
        self.engineer_combo.move(413, 336)
        self.engineer_combo.resize(275, 50)
        self.engineer_combo.setPlaceholderText('Инженер по подбору')
        self.engineer_combo.activated[str].connect(self._onEngineerActivated)

        self.lPhoneNumber = QLabel(self)
        self.lPhoneNumber.move(717, 295)
        self.lPhoneNumber.resize(275, 53)
        self.lPhoneNumber.setText('Контактная информация')
        self.lPhoneNumber.setFont(QFont(Circle_Regular, 15))
        self.lPhoneNumber.setStyleSheet('''color: White''')
        self.lPhoneNumber.resize(275, 53)
        self.inPhoneNumber = QLabel(self)
        self.inPhoneNumber.move(717, 336)
        self.inPhoneNumber.resize(275, 53)
        self.inPhoneNumber.setStyleSheet("color: White; background-color: rgb(223, 104, 98)")
        # self.inPhoneNumber.setPlaceholderText('Контактная информация')
        self.inPhoneNumber.setFont(QFont(Circle_Regular, 15))

        self.butLeft1 = QPushButton('Назад', self)
        self.butLeft1.move(108, 447)
        self.butLeft1.resize(104, 50)
        self.butLeft1.setFont(QFont(Circle_Regular, 15))

        self.butLeft2 = QPushButton('Назад', self)
        self.butLeft2.move(108, 447)
        self.butLeft2.resize(104, 50)
        self.butLeft2.setFont(QFont(Circle_Regular, 15))
        self.butLeft2.hide()

        self.butNext1 = QPushButton('Далее', self)
        self.butNext1.setFont(QFont(Circle_Regular, 15))
        self.butNext1.move(888, 447)
        self.butNext1.resize(104, 50)
        self.butNext1.setStyleSheet("QPushButton {background-color: rgb(235,86,79); color: White; border-radius: 1px;}"
                                    "QPushButton:pressed {background-color:rgb(251,114,107) ; }")

        self.butLeft1.enterEvent = self.onCursor
        self.butLeft1.leaveEvent = self.offCursor
        self.butLeft2.enterEvent = self.onCursor
        self.butLeft2.leaveEvent = self.offCursor
        self.butNext1.enterEvent = self.onCursor
        self.butNext1.leaveEvent = self.offCursor
        self.SetNormalSize()

    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return False

    def _onEngineerActivated(self, text):
        try:
            self.inPhoneNumber.setText(DataManager.sql_query("SELECT contact FROM users WHERE name='" + text + "';")[0][0])
        except:
            self.messageboxerror("Ошибка подключения к базе данных")
    def clean_page(self):
        self.inCompany.clear()
        self.inBush.clear()
        self.inWell.clear()
        self.inField.clear()

    """def paintEvent(self, e):
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
"""
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