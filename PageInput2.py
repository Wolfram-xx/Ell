from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QCursor
from PyQt5.Qt import QFontDatabase

class PageInput2(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.koefW, self.koefH = 1, 1
        shadow = QGraphicsDropShadowEffect(self,
                                           blurRadius=35,
                                           color=QColor(0, 0, 0, 35),
                                           offset=QPointF(10, 10),
                                           )
        self.setGraphicsEffect(shadow)
        fontId = QFontDatabase.addApplicationFont("Fonts/Circe-Regular.ttf")
        Circle_Regular = QFontDatabase.applicationFontFamilies(fontId)[0]

        self.lTitle = QLabel(self)
        self.lTitle.move(70, 27)
        self.lTitle.setStyleSheet('''color: White''')
        self.lTitle.setText("Создание нового проекта")
        self.lTitle.resize(1000, 50)

        self.lDownhole1 = QLabel(self)
        self.lDownhole1.move(70, 120)
        self.lDownhole1.resize(180, 20)
        self.lDownhole1.setText('Забой скважины(проект) MD')
        self.inDownhole11 = QLineEdit(self)
        self.inDownhole11.move(250, 110)
        self.inDownhole11.resize(50, 40)
        self.inDownhole11.setPlaceholderText('MD')
        self.lDownhole112 = QLabel(self)
        self.lDownhole112.move(300, 120)
        self.lDownhole112.setText('м  TVD')

        self.inDownhole12 = QLineEdit(self)
        self.inDownhole12.move(350, 110)
        self.inDownhole12.resize(50, 40)
        self.inDownhole12.setPlaceholderText('TVD')
        self.lDownhole122 = QLabel(self)
        self.lDownhole122.move(400, 120)
        self.lDownhole122.setText('м')

        self.lDownhole21 = QLabel(self)
        self.lDownhole21.move(70, 170)
        self.lDownhole21.resize(180, 20)
        self.lDownhole21.setText('Забой скважины(факт) MD')
        self.inDownhole21 = QLineEdit(self)
        self.inDownhole21.move(250, 160)
        self.inDownhole21.resize(50, 40)
        self.inDownhole21.setPlaceholderText('MD')
        self.lDownhole212 = QLabel(self)
        self.lDownhole212.move(300, 170)
        self.lDownhole212.setText('м  TVD')

        self.inDownhole22 = QLineEdit(self)
        self.inDownhole22.move(350, 160)
        self.inDownhole22.resize(50, 40)
        self.inDownhole22.setPlaceholderText('TVD')
        self.lDownhole222 = QLabel(self)
        self.lDownhole222.move(400, 170)
        self.lDownhole222.setText('м')

        self.lDiamOpenBarrel = QLabel(self)
        self.lDiamOpenBarrel.move(70, 220)
        self.lDiamOpenBarrel.resize(180, 20)
        self.lDiamOpenBarrel.setText('Диаметр открытого ствола')
        self.inDiamOpenBarrel = QLineEdit(self)
        self.inDiamOpenBarrel.move(250, 210)
        self.inDiamOpenBarrel.resize(50, 40)
        self.lDiamOpenBarrel2 = QLabel(self)
        self.lDiamOpenBarrel2.move(300, 220)
        self.lDiamOpenBarrel2.setText('мм')

        self.lOffsetFromVert = QLabel(self)
        self.lOffsetFromVert.move(70, 270)
        self.lOffsetFromVert.resize(180, 20)
        self.lOffsetFromVert.setText('Смещение от вертикали')
        self.inOffsetFromVert = QLineEdit(self)
        self.inOffsetFromVert.move(250, 260)
        self.inOffsetFromVert.resize(50, 40)
        self.lOffsetFromVert2 = QLabel(self)
        self.lOffsetFromVert2.move(300, 270)
        self.lOffsetFromVert2.setText('м')

        self.lLenBarrel = QLabel(self)
        self.lLenBarrel.move(70, 320)
        self.lLenBarrel.resize(180, 20)
        self.lLenBarrel.setText('Длина необсаженного ствола')
        self.inLenBarrel = QLineEdit(self)
        self.inLenBarrel.move(250, 310)
        self.inLenBarrel.resize(50, 40)
        self.lLenBarrel2 = QLabel(self)
        self.lLenBarrel2.move(300, 320)
        self.lLenBarrel2.setText('м')

        self.lCorner = QLabel(self)
        self.lCorner.move(70, 370)
        self.lCorner.resize(180, 20)
        self.lCorner.setText('Максимальный зенитный угол')
        self.inCorner = QLineEdit(self)
        self.inCorner.move(250, 360)
        self.inCorner.resize(50, 40)

        self.lInterval = QLabel(self)
        self.lInterval.move(300, 370)
        self.lInterval.setText('º в интервале')
        self.inInterval = QLineEdit(self)
        self.inInterval.move(385, 360)
        self.inInterval.resize(50, 40)
        self.lInterval2 = QLabel(self)
        self.lInterval2.move(435, 370)
        self.lInterval2.setText('м')

        self.lTypeWell = QLabel(self)
        self.lTypeWell.move(450, 120)
        self.lTypeWell.setText('Тип скважины')
        self.inTypeWell = QComboBox(self)
        self.inTypeWell.addItem('Горизонтальная')
        self.inTypeWell.addItem('ЗБС')
        self.inTypeWell.addItem('Наклонно-направленная')
        self.inTypeWell.addItem('Вертикальная')
        self.inTypeWell.addItem('Многоствольная')
        self.inTypeWell.move(600, 110)
        self.inTypeWell.resize(130, 40)

        self.lReservoirPres = QLabel(self)
        self.lReservoirPres.move(450, 170)
        self.lReservoirPres.resize(180, 20)
        self.lReservoirPres.setText('Пластовое давление')
        self.inReservoirPres = QLineEdit(self)
        self.inReservoirPres.move(600, 160)
        self.inReservoirPres.resize(70, 40)
        self.lReservoirPres2 = QLabel(self)
        self.lReservoirPres2.move(670, 170)
        self.lReservoirPres2.resize(100, 40)
        self.lReservoirPres2.setText('МПа')

        self.lWellHeadPres = QLabel(self)
        self.lWellHeadPres.move(450, 220)
        self.lWellHeadPres.resize(180, 20)
        self.lWellHeadPres.setText('Устьевое давление')
        self.inWellHeadPres = QLineEdit(self)
        self.inWellHeadPres.move(600, 210)
        self.inWellHeadPres.resize(70, 40)
        self.lWellHeadPres2 = QLabel(self)
        self.lWellHeadPres2.move(670, 220)
        self.lWellHeadPres2.setText('МПа')

        self.lDesInterShank = QLabel(self)
        self.lDesInterShank.move(450, 270)
        self.lDesInterShank.resize(180, 20)
        self.lDesInterShank.setText('Интервал спуска хвостовика')
        self.inDesInterShank = QLineEdit(self)
        self.inDesInterShank.move(600, 260)
        self.inDesInterShank.resize(70, 40)
        self.lDesInterShank2 = QLabel(self)
        self.lDesInterShank2.move(670, 270)
        self.lDesInterShank2.setText('мм')

        self.lNumberStages = QLabel(self)
        self.lNumberStages.move(450, 320)
        self.lNumberStages.resize(180, 20)
        self.lNumberStages.setText('Кол-во стадий ГРП')
        self.inNumberStages = QLineEdit(self)
        self.inNumberStages.move(600, 310)
        self.inNumberStages.resize(70, 40)
        self.inNumberStages.setText("1")

        self.lthread = QLabel(self)
        self.lthread.move(450, 370)
        self.lthread.resize(180, 20)
        self.lthread.setText("Тип резьбы")
        self.thread_combo = QComboBox(self)
        self.thread_combo.addItem("ОТТМ")
        self.thread_combo.addItem("ТМК")
        self.thread_combo.addItem("ВС")
        self.thread_combo.addItem("ОТТГ")
        self.thread_combo.move(600, 360)
        self.thread_combo.resize(70, 40)

        # self.lEx = QLabel(self)
        # self.lEx.move(700, 20)
        # self.lEx.resize(180, 20)
        # self.lEx.setText('Эксплуатационная колонна')

        self.lOuterDiam = QLabel(self)
        self.lOuterDiam.move(750, 170)
        self.lOuterDiam.resize(180, 20)
        self.lOuterDiam.setText('Диаметр внешний')
        self.inOuterDiam = QLineEdit(self)
        self.inOuterDiam.move(890, 160)
        self.inOuterDiam.resize(50, 40)
        self.lOuterDiam2 = QLabel(self)
        self.lOuterDiam2.move(940, 170)
        self.lOuterDiam2.setText('мм')

        self.lInnerDiam = QLabel(self)
        self.lInnerDiam.move(750, 220)
        self.lInnerDiam.resize(180, 20)
        self.lInnerDiam.setText('Диаметр внутренний')
        self.inInnerDiam = QLineEdit(self)
        self.inInnerDiam.move(890, 210)
        self.inInnerDiam.resize(50, 40)
        self.lInnerDiam2 = QLabel(self)
        self.lInnerDiam2.move(940, 220)
        self.lInnerDiam2.setText('мм')

        self.lDescentDepth = QLabel(self)
        self.lDescentDepth.move(750, 270)
        self.lDescentDepth.resize(180, 20)
        self.lDescentDepth.setText('Глубина спуска')
        self.inDescentDepth = QLineEdit(self)
        self.inDescentDepth.move(890, 260)
        self.inDescentDepth.resize(50, 40)
        self.lDescentDepth2 = QLabel(self)
        self.lDescentDepth2.move(940, 270)
        self.lDescentDepth2.setText('м')

        self.lDepthCCODE = QLabel(self)
        self.lDepthCCODE.move(750, 320)
        self.lDepthCCODE.resize(180, 20)
        self.lDepthCCODE.setText('Глубина ЦКОД')
        self.inDepthCCODE = QLineEdit(self)
        self.inDepthCCODE.move(890, 310)
        self.inDepthCCODE.resize(50, 40)
        self.lDepthCCODE2 = QLabel(self)
        self.lDepthCCODE2.move(940, 320)
        self.lDepthCCODE2.setText('м')

        self.lcompon = QLabel(self)
        self.lcompon.move(750, 370)
        self.lcompon.resize(180, 20)
        self.lcompon.setText('Тип компоновки')
        self.compon_combo = QComboBox(self)
        self.compon_combo.addItem('Strike NC')
        self.compon_combo.addItem('Strike RC')
        self.compon_combo.addItem('Strike RT')
        self.compon_combo.addItem('Solvtech')
        self.compon_combo.addItem('Shuttle')
        self.compon_combo.addItem('Spectr')
        self.compon_combo.move(890, 360)
        self.compon_combo.resize(130, 40)
        # self.compon_combo.activated[str].connect(self.onActivated)

        self.butLeft2 = QPushButton('Назад', self)
        self.butLeft2.move(108, 447)
        self.butLeft2.resize(104, 50)

        self.butNext2 = QPushButton('Создать', self)
        self.butNext2.move(888, 447)
        self.butNext2.resize(104, 50)
        self.butNext2.setStyleSheet("QPushButton {background-color: rgb(235,86,79); color: White; border-radius: 1px;}"
                                    "QPushButton:pressed {background-color:rgb(251,114,107) ; }")

        for i in self.children():
            if (i.__class__ == QLineEdit or i.__class__ == QLabel or i.__class__ == QComboBox or i.__class__ == QPushButton):
                i.setFont(QFont(Circle_Regular, 12))

        self.lTitle.setFont(QFont(Circle_Regular, 25))
        self.butNext2.setFont(QFont(Circle_Regular, 15))
        self.butLeft2.setFont(QFont(Circle_Regular, 15))

        self.butLeft2.enterEvent = self.onCursor
        self.butLeft2.leaveEvent = self.offCursor
        self.butNext2.enterEvent = self.onCursor
        self.butNext2.leaveEvent = self.offCursor
        self.SetNormalSize()

    def clean_page(self):
        self.inDownhole11.setText("")
        self.inDownhole12.setText("")
        self.inDownhole21.setText("")
        self.inDownhole22.setText("")
        self.inNumberStages.setText("")

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
