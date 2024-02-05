from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import DataManager
import subprocess
import copy

class BigSheme(QWidget):
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

        self.index = 0
        self.details = []
        self.tab = ""
        self.pashref = "passports"
        self.id_project = 0
        self.id_detail = 0
        self.flagAboutChangeDetail = False

        self.label = QLabel(self)
        self.label.move(300, 5)
        self.label.resize(100, 500)
        self.label.setAlignment(Qt.AlignCenter)


        self.Number = QLabel(self)
        self.Number.setText("0")
        self.Number.move(70, 20)
        self.Number.resize(30, 19)
        self.Number.setFont(QFont(Circle_Regular, 14))
        self.Number.setStyleSheet("color:White")
        """self.hesh = QLabel("#", self)
        self.hesh.move(58, 453)
        self.hesh.destroy()"""


        self.name = QLabel(self)
        self.name.move(500, 50)
        self.name.resize(1200, 20)

        self.number = QLabel(self)
        self.number.move(500, 70)
        self.number.resize(1200, 20)

        self.length = QLabel(self)
        self.length.move(500, 160)
        self.length.resize(1200, 20)

        self.OD = QLabel(self)
        self.OD.move(500, 140)
        self.OD.resize(1200, 20)

        self.ID = QLabel(self)
        self.ID.move(500, 120)
        self.ID.resize(1200, 20)

        self.passporthref = QPushButton("открыть паспорт", self)
        self.passporthref.move(500, 180)
        self.passporthref.resize(120, 20)
        self.passporthref.clicked.connect(self.openpassportinbrowser)

        self.newcomp = QPushButton("Добавить новую", self)
        self.newcomp.move(500, 220)
        self.newcomp.resize(120, 20)

        self.another = QTableWidget(self)
        self.another.move(500, 300)
        self.another.resize(200, 100)
        self.another.verticalHeader().hide()
        self.another.horizontalHeader().hide()
        self.another.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.another.setSelectionMode(QAbstractItemView.SingleSelection)
        self.another.setStyleSheet("QTableWidget { border: none } QTableWidget::item { background-color: rgba(0, 0, 0, 5) }")
        self.lanother = QLabel(self)
        self.lanother.move(500, 280)


        self.NextBut = QPushButton(">", self)
        self.NextBut.resize(52, 530)
        self.NextBut.move(1020, 0)
        self.NextBut.clicked.connect(self.nextImg)

        self.BackBut = QPushButton("<", self)
        self.BackBut.resize(50, 470)
        self.BackBut.move(0, 60)
        self.BackBut.clicked.connect(self.backImg)

        self.BackBackBut = QPushButton("Назад", self)
        self.BackBackBut.resize(50, 50)
        self.BackBackBut.move(0, 0)

        # вид курсора
        self.BackBackBut.enterEvent = self.onCursor
        self.BackBackBut.leaveEvent = self.offCursor
        self.BackBut.enterEvent = self.onCursor
        self.BackBut.leaveEvent = self.offCursor
        self.NextBut.enterEvent = self.onCursor
        self.NextBut.leaveEvent = self.offCursor
        self.newcomp.enterEvent = self.onCursor
        self.newcomp.leaveEvent = self.offCursor
        self.passporthref.enterEvent = self.onCursor
        self.passporthref.leaveEvent = self.offCursor
        self.another.enterEvent = self.onCursor
        self.another.leaveEvent = self.offCursor
        self.SetNormalSize()

    # меняет на выбраное из таблицы оборудование
    def changePlaceDetails(self, ind):
        DataManager.sql_query(f"UPDATE Details SET id_img='{self.an_details[ind][0]}' WHERE id_img='{self.id_detail}' AND id_project={self.id_project};")

    def updatePage(self):
        self.setImage(self.details)

        # ищет и выводит в таблицу похожее оборудование

    def findanotherdetail(self, code, id, tab):
        match code:
            case 510 | 511 | 418 | 405 | 413 | 610 | 611 | 557:
                return DataManager.sql_query(
                    f"SELECT * FROM Compon WHERE code LIKE '{code}%' AND NOT id='{id}' AND (thread_type='{tab[0:6]+tab[9:len(tab)]}' OR thread_type='{tab}');")
            case 502 | 505 | 564 | 552 | 579 | 531 | 533 | 554 | 560 | 146 | 241 | 501 | 935:
                return DataManager.sql_query(
                    f"SELECT * FROM Compon WHERE code LIKE '{code}%' AND NOT id='{id}' AND thread_type='{tab}';")

    def searchAnotherDetails(self, number):
        if self.id_detail != 54 and self.id_detail != 55:
            self.an_details = self.findanotherdetail(int(number[0:3]), self.id_detail, str(self.tab))
        else:
            self.an_details = []
        if self.an_details:
            details = self.an_details
            self.another.setRowCount(len(details))
            self.another.setColumnCount(1)
            self.another.resize(200, 40*len(details))
            for i in range(len(details)):
                self.another.setColumnWidth(i, 0)
                self.another.setItem(i, 0, QTableWidgetItem(details[i][1]))
            self.another.resizeColumnsToContents()
            self.lanother.show()
            self.another.show()
            self.lanother.setText("Похожие:")
        else:
            self.lanother.hide()
            self.another.hide()

    def openpassportinbrowser(self):
        path = str(self.details[self.index][8])
        if path != None:
            subprocess.Popen([path], shell=True)



    def setImage(self, details):
        self.another.clearSelection()
        img = QPixmap(details[self.index][4])
        self.label.setPixmap(img.scaled(100, 400, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.name.setText(details[self.index][2])
        self.number.setText(details[self.index][3])
        self.ID.setText("Наружный диаметр: " + str(details[self.index][5]) + " мм")
        self.OD.setText("Внутренний диаметр: " + str(details[self.index][6]) + " мм")
        self.length.setText("Длина: " + str(details[self.index][7]) + " мм")
        st = details[self.index][8]
        s = st.rfind("/")
        self.pashref = st[s+1:]
        self.id_detail = self.details[self.index][0]
        self.searchAnotherDetails(details[self.index][3])
        self.Number.setText("" + str(details[self.index][1]))

    def nextImg(self):
        if (self.index < len(self.details) - 1):
            self.index += 1
            self.setImage(self.details)

    def backImg(self):
        if (self.index > 0 and self.index < len(self.details) + 1):
            self.index -= 1
            self.setImage(self.details)

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
        qp.drawRoundedRect(int(200 * self.koefW), int(40 * self.koefH), int(700 * self.koefW), int(420 * self.koefH), 10, 10)   # Рисование прямоугольника


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