import sys
import time
from datetime import datetime
import DataManager
from WorkWithFiles import save_inzip, copyfile
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
import OpenExFile
import FileCreating
from SaveDataForOlimp import SaveDataForOlimp
from Data import Data
from PIL import Image, ImageDraw
import copy

PrIn = Data.ProjectInfo()
HoIn = Data.HoleInfo()
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


class Delegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() == 5:
            return super(Delegate, self).createEditor(parent, option, index)
def paintIMGsmall(img):
    return img.scaled(120, 1000, Qt.KeepAspectRatio, Qt.FastTransformation)


class ClickedWid(QWidget):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()

class ClickedLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()

class PageOutput(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self._setZeroValues()
        self.butRequest = QPushButton("Запрос ПЗ", self)
        self.butRequest.move(800, 60)
        self.butRequest.resize(70,  40)
        self.butRequest.clicked.connect(self.SDFO)

        self.butInput = QPushButton("Ввод ПЗ", self)
        self.butInput.move(880, 60)
        self.butInput.resize(70, 40)
        self.butInput.clicked.connect(self.butInput_Clicked)

        self.butSavePassportInZip = QPushButton("Собрать все паспорта", self)
        self.butSavePassportInZip.move(800, 120)
        self.butSavePassportInZip.resize(150, 40)

        self.StatusBut = QPushButton("О\nт\nк\nр\nы\nт\nь\n \nс\nт\nа\nт\nу\nс\nы", self)
        self.StatusBut.resize(25, 210)
        self.StatusBut.move(800, 260)
        self.StatusBut.x0 = 800
        self.StatusBut.x1 = 800
        self.StatusBut.clicked.connect(self.StatusClicked)

        self.check1 = QCheckBox(self)
        self.check1.move(820, 265)
        self.check1.hide()
        self.check1.clicked.connect(self.StatusCheckBox)
        self.check2 = QCheckBox(self)
        self.check2.move(820, 318)
        self.check2.hide()
        self.check2.clicked.connect(self.StatusCheckBox)
        self.check3 = QCheckBox(self)
        self.check3.move(820, 381)
        self.check3.hide()
        self.check3.clicked.connect(self.StatusCheckBox)
        self.check4 = QCheckBox(self)
        self.check4.move(820, 435)
        self.check4.hide()
        self.check4.clicked.connect(self.StatusCheckBox)

        self.check1L = QLabel("Excel «Схема хвостовика»", self)
        self.check1L.move(840, 265)
        self.check1L.resize(150, 30)
        self.check1L.hide()
        self.check2L = QLabel("Коммерческое предложение", self)
        self.check2L.resize(150, 30)
        self.check2L.move(840, 318)
        self.check2L.hide()
        self.check3L = QLabel("Статус выиграно", self)
        self.check3L.move(840, 381)
        self.check3L.hide()
        self.check4L = QLabel("Статус проиграно", self)
        self.check4L.move(840, 435)
        self.check4L.hide()

        self.lCost = QLabel(self)
        self.lCost.move(800, 170)
        self.lCost.setText("Стоимость реализации:")
        self.lCost.resize(150, 20)
        self.lCost.setStyleSheet("color: White")
        self.inCost = QLineEdit(self)
        self.inCost.move(800, 200)
        self.inCost.resize(100, 20)
        self.inCost.setText(str(self.cost) + "тыс. руб")
        self.refreshCost = QPushButton(self)
        self.refreshCost.move(930, 200)
        self.refreshCost.resize(20, 20)
        self.refreshCost.clicked.connect(self._updateCost)


        self.lbl = QLabel(self)
        self.lbl.move(10, -10)
        self.lbl.resize(400, 30)
        self.lbl.setText("Strike NC 178-OTTM114")
        self.lbl.setStyleSheet("color: White")
        self.lbl.hide()

        self.saveas = QComboBox(self)
        self.saveas.addItem("Сохранить как...")
        self.saveas.addItem("PDF")
        self.saveas.addItem("XLSX")
        self.saveas.move(800, 20)
        self.saveas.resize(150, 20)



        # Создание таблички элементов
        self.table = QTableWidget(self)
        self.table.move(230, 270)
        self.table.resize(560, 200)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.verticalHeader().hide()
        self.table.setStyleSheet('.QWidget {background-color: White')
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tablecount = QTableWidget(self)
        self.tablecount.move(230, 270)
        self.tablecount.resize(560, 200)
        self.tablecount.verticalHeader().hide()
        self.tablecount.setStyleSheet('.QWidget {background-color: White')

        self.tablewidg = QTabWidget(self)
        self.tablewidg.move(230, 240)
        self.tablewidg.resize(560, 230)
        self.tablewidg.addTab(self.table, "Данные по компоновке")
        self.tablewidg.addTab(self.tablecount, "Данные по оборудованию")


        # Создание поля с картинками
        self.scrollarea = QScrollArea(self)
        self.shemeWid = ClickedWid(self)
        self.schemeLayout = QVBoxLayout(self)
        self.shemeWid.setLayout(self.schemeLayout)
        self.shemeWid.setStyleSheet('.QWidget {background-color: White')

        # Настройка
        self.scrollarea.setWidget(self.shemeWid)
        self.scrollarea.setGeometry(0, 0, 150, 450)
        self.scrollarea.setMinimumSize(150, 450)
        self.scrollarea.setMaximumSize(170, 1000)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollarea.move(10, 20)
        self.shemeWid.resize(200, 100)

        self.lprojectInfo = QLabel(self)
        self.lprojectInfo.move(230, -10)
        self.lprojectInfo.resize(400, 30)
        self.lprojectInfo.setText('Общая информация')
        self.lprojectInfo.setStyleSheet("color: White")
        self.projectInfo = QTableWidget(self)
        self.projectInfo.setSelectionMode(QTableWidget.NoSelection)
        self.projectInfo.setColumnCount(4)
        self.projectInfo.setRowCount(5)
        self.projectInfo.resize(560, 200)
        self.projectInfo.move(230, 20)
        self.projectInfo.setStyleSheet('.QWidget {background-color: White')

        self.projectInfo.setItem(0, 0, QTableWidgetItem("Компания"))
        self.projectInfo.setItem(0, 2, QTableWidgetItem("Месторождение"))
        self.projectInfo.setItem(1, 0, QTableWidgetItem("Скважина"))
        self.projectInfo.setItem(1, 2, QTableWidgetItem("Куст"))
        self.projectInfo.setItem(2, 0, QTableWidgetItem("Инженер"))
        self.projectInfo.setItem(2, 2, QTableWidgetItem("Контакт инженера"))
        self.projectInfo.setItem(3, 0, QTableWidgetItem("Дата подбора"))
        self.projectInfo.setItem(3, 2, QTableWidgetItem("Кол-во стадий ГРП"))
        self.projectInfo.setItem(4, 0, QTableWidgetItem("Общая длина"))
        self.projectInfo.setItem(4, 2, QTableWidgetItem("Дата формирования цены"))
        self.projectInfo.verticalHeader().hide()
        self.projectInfo.horizontalHeader().hide()
        self.projectInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.projectInfo.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.projectInfo.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.butLeft = QPushButton('Назад', self)
        self.butLeft.move(10, 500)
        self.butLeft.hide()
        self.butLeftCreateProject = QPushButton('Выйти к списку проектов', self)
        self.butLeftCreateProject.move(820, 480)
        self.butLeftCreateProject.resize(150, 40)

        self.butLeftCreateProject.hide()
        self.lCost.hide()
        self.inCost.hide()
        self.refreshCost.hide()

        self.saveas.currentIndexChanged.connect(self.saveasClicked)
        self.butSavePassportInZip.clicked.connect(self.save_passportinzip)
        delegate = Delegate(self.tablecount)
        self.tablecount.setItemDelegate(delegate)

        self.butRequest.enterEvent = self.onCursor
        self.butRequest.leaveEvent = self.offCursor
        self.butInput.enterEvent = self.onCursor
        self.butInput.leaveEvent = self.offCursor
        self.butSavePassportInZip.enterEvent = self.onCursor
        self.butSavePassportInZip.leaveEvent = self.offCursor
        self.butLeft.enterEvent = self.onCursor
        self.butLeft.leaveEvent = self.offCursor
        self.butLeftCreateProject.enterEvent = self.onCursor
        self.butLeftCreateProject.leaveEvent = self.offCursor
        self.SetNormalSize()


    def _setZeroValues(self):
        self.status = False
        self.koefW = 1
        self.koefH = 1
        self.statusW = 0
        self.details = []
        self.countandcost_details = []
        self.place_img = []
        self.id_project = 2
        self.cost = 0
        self.percent = 40
        self.FlagPrimaryCosts = False
        self.project = []
        self.id = 2
        self.countDetails = 0
        self.Date = ""
        self.tab = ""
        self.FlagChTabl = False
        self.statuses = []
        self.id_status = 0
    def messageboxerror(self, text):
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return False

    def save_passportinzip(self):
        files = []
        for i in range(2, len(self.countandcost_details)):
            files.append(self.countandcost_details[i][4])
        save_inzip(files)

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
        qp.drawRoundedRect(int(800 * self.koefW), int(260 * self.koefH), int(25 * self.koefW * self.statusW), int(210 * self.koefH), 10, 10)   # Рисование прямоугольника
    def StatusClicked(self):
        if self.status:
            self.check1.hide()
            self.check2.hide()
            self.check3.hide()
            self.check4.hide()
            self.check1L.hide()
            self.check2L.hide()
            self.check3L.hide()
            self.check4L.hide()
            self.status = False

            for i in range(1, 11):
                self.statusW = 11 - i
                self.StatusBut.move(int(self.StatusBut.x1 - i * 25 * self.koefW), int(260 * self.koefH))
                t = time.time()
                while time.time() < t + 0.03:
                    QCoreApplication.processEvents()
                self.update()
            self.StatusBut.setText("О\nт\nк\nр\nы\nт\nь\n \nс\nт\nа\nт\nу\nс\nы")
            self.StatusBut.x0 = 800
            self.StatusBut.x1 = int(800 * self.koefW)
            self.statusW = 0
        else:
            for i in range(1, 11):
                self.statusW = i
                self.StatusBut.move(int(self.StatusBut.x1 + i * 25 * self.koefW), int(260 * self.koefH))
                t = time.time()
                while time.time() < t + 0.03:
                    QCoreApplication.processEvents()
                self.update()
            self.StatusBut.setText("С\nк\nр\nы\nт\nь\n \nс\nт\nа\nт\nу\nс\nы")

            self.check1.show()
            self.check2.show()
            self.check3.show()
            self.check4.show()
            self.check1L.show()
            self.check2L.show()
            self.check3L.show()
            self.check4L.show()
            self.status = True
            self.StatusBut.x0 = 1050
            self.StatusBut.x1 = int(1050 * self.koefW)



    def StatusCheckBox(self):
        st = [self.check1.isChecked(), self.check2.isChecked(), self.check3.isChecked(), self.check4.isChecked()]
        for i in range(len(st)):
            if self.statuses[i+1] != str(st[i]):
                DataManager.sql_query(f"UPDATE Statuses SET status{i+1}='{st[i]}' WHERE id={self.id_status};")

    def getstatusesproject(self):
        self.id_status = DataManager.sql_query(f"SELECT id_status FROM Project WHERE id={self.id};")[0][0]
        self.statuses = DataManager.sql_query(f"SELECT * FROM Statuses WHERE id={self.id_status};")[0]
        if self.statuses[1] == 'True':
            self.check1.setChecked(True)
        else:
            self.check1.setChecked(False)
        if self.statuses[2] == 'True':
            self.check2.setChecked(True)
        else:
            self.check2.setChecked(False)
        if self.statuses[3] == 'True':
            self.check3.setChecked(True)
        else:
            self.check3.setChecked(False)
        if self.statuses[4] == 'True':
            self.check4.setChecked(True)
        else:
            self.check4.setChecked(False)


    def saveasClicked(self):
        try:
            match self.saveas.currentText():
                case "PDF":
                    cost_details = []
                    if self.tablecount.columnCount() != 4:
                        for i in range(len(self.countandcost_details)):
                            cost_details.append(self.tablecount.item(i, 6).text().split()[0])
                    else:
                        self.messageboxerror("Извините, без ПЗ нельзя составить коммерческое предложение")
                        self.saveas.setCurrentIndex(0)
                        return
                    print(6678)
                    commercialOfferNumber = (QInputDialog.getText(self, 'Введите данные', 'Номер коммерческого предложения:'))[0]
                    wellConditions = (QInputDialog.getText(self, 'Введите данные', 'Скважинные условия:'))[0]
                    d = f'{datetime.now().date()}'
                    d = d.split('-')
                    print(1556)
                    Date = f'{d[2]}.{d[1]}.{d[0]}'
                    Data = [PrIn.Company, PrIn.Well, HoIn.NumberOfStagesGRP,
                            PrIn.Field, PrIn.Engineer, Date,
                            PrIn.ContactEngineer, HoIn.OpenHoleDiameter, HoIn.ReservoirPressure,
                            self.details, HoIn.CompositionType, wellConditions,
                            self.countandcost_details, cost_details, commercialOfferNumber]
                    FileCreating.NewFile(self, "PDF", Data)
                    self.saveas.setCurrentIndex(0)
                case "XLSX":
                    Data = [PrIn.Company, PrIn.Well, HoIn.NumberOfStagesGRP,
                            PrIn.Field, PrIn.Engineer, PrIn.Date,
                            PrIn.ContactEngineer, HoIn.OpenHoleDiameter, HoIn.ReservoirPressure,
                            self.details]
                    FileCreating.NewFile(self, "XLSX", Data)
                    self.saveas.setCurrentIndex(0)
                case "Сохранить как...":
                    pass
        except:
            self.saveas.setCurrentIndex(0)
            self.messageboxerror("12312412")

    def SDFO(self):
        textfromdialwin = QInputDialog.getText(self, 'Введите данные', 'Месяц производства:')
        if textfromdialwin[1]:
            nomenclature = []
            count = []
            client = PrIn.Company
            monthOfProduction = textfromdialwin[0]
            for det in self.countandcost_details:
                count.append(str(det[3]))
                nomenclature.append(det[2])
            count.reverse()
            nomenclature.reverse()
            SaveDataForOlimp({
                            'Заказчик': [client],
                            'Месяц производства': [monthOfProduction]
                            },
                            {
                            'Шифр': nomenclature,
                            'Кол-во': count
                            })

    def SearchCostDetail(self, path, i):
        numCom = str(self.countandcost_details[i][2])
        return str(OpenExFile.FindPrice(numCom, path))

    def write_costindb(self, path):
        for i in range(self.countsimilarpassport()):
            primarycost = self.SearchCostDetail(path, i)
            id_img = DataManager.sql_query(f"SELECT id_img FROM Details WHERE id_project='{self.id}' AND place='{self.countandcost_details[i][7]}';")
            if id_img:
                id_img = id_img[0][0]
            ids_detail = DataManager.sql_query(f"SELECT id FROM Details WHERE id_project='{self.id}' AND id_img='{id_img}';")
            for d in ids_detail:
                DataManager.sql_query(
                    f"UPDATE Details SET primary_cost={primarycost} WHERE id='{d[0]}';")
                DataManager.sql_query(
                    f"UPDATE Details SET profitability=40 WHERE id='{d[0]}';")
            self._updateCost()


    def butInput_Clicked(self):
        self.Date = datetime.now()
        self.cost = 0
        self.FlagPrimaryCosts = True
        path = OpenExFile.OpenFileEXL()
        if (path != None):
            DataManager.sql_query(f"UPDATE Project SET date_cost='{str(self.Date.date())}' WHERE id='{str(self.id)}';")
            self.projectInfo.setItem(4, 3, QTableWidgetItem(self.dateChange(str(self.Date.date()))))
            self.lCost.show()
            self.refreshCost.show()
            self.inCost.show()
            self.write_costindb(path)
            DataManager.sql_query(f"UPDATE Project SET all_cost='{str(self.cost)}' WHERE id='{str(self.id)}';")
            self.getImagesDetails()
            self.details.reverse()
            self.printProdTables()
            self.tablecount.resizeColumnsToContents()
            self._updateCost()


    def QMouseEvent(self, event):
        self.c.closeApp.emit()

    def on_selectionChanged(self, selected):
        r = 0
        c = 0
        for i in selected.indexes():
            r = i.row()
            c = i.column()
            if c == 5:
                self.FlagChTabl = True
            else:
                self.FlagChTabl = False

    def validateFloat(self, st):
        try:
            if (st != ""):
                float(st)
            else:
                return False
            return True
        except BaseException:
            return False
    def cellchangedtable(self, row, column):
        if column == 5 and self.FlagChTabl:
            t1 = self.tablecount.item(row, 4).text().split(" ")[0]
            t = self.validateFloat(self.tablecount.item(row, 5).text().split(" ")[0])
            id_detInformation = DataManager.sql_query(
                f"SELECT id_img, profitability FROM Details WHERE id_project='{self.id}' AND place='{self.countandcost_details[row][7]}';")
            if t:
                t2 = float(self.tablecount.item(row, 5).text().split(" ")[0])
                if t2 < 10 or t2 > 40:
                    self.tablecount.item(row, 5).setText(f"{id_detInformation[0][1]}")
                    return
            else:
                self.tablecount.item(row, 5).setText(f"{id_detInformation[0][1]}")
                return
            t3 = self.tablecount.item(row, 6).text().split(" ")[0]
            profitability = round(((100 + t2)*float(t1))/100, 2)
            if int(self.tablecount.item(row, 3).text()) > 1:
                self.tablecount.setItem(row, 6, QTableWidgetItem(str(profitability) + " (" + str(profitability / float(self.tablecount.item(row, 3).text())) + "/шт)"))
            else:
                self.tablecount.setItem(row, 6, QTableWidgetItem(str(profitability)))
            self._updateCost()
            self.tablecount.resizeColumnsToContents()
            id_img = id_detInformation[0][0]
            ids_detail = DataManager.sql_query(
                f"SELECT id FROM Details WHERE id_project='{self.id}' AND id_img='{id_img}';")
            for d in ids_detail:
                DataManager.sql_query(
                    f"UPDATE Details SET profitability={t2} WHERE id='{d[0]}';")


    def _updateCost(self):
        cost = 0
        for i in range(self.tablecount.rowCount()):
            cost += float(self.tablecount.item(i, 6).text().split(" ")[0])
        self.inCost.setText(str(round(cost, 1)))
        self.cost = cost


    def heightimg(self, img):
        with Image.open(img) as img_1:
            img_1.load()
        h = (img_1.height * 150) // img_1.width
        return h

    # отрисовывает картинки в блоке
    def drawsSheme(self):
        len = 0
        for i in range(self.countDetails):
            len = len + self.heightimg(self.details[i][4])
        self.shemeWid.resize(200, self.countDetails * 2 + len)
        self.details.reverse()
        for i in range(self.countDetails):
            self.createimg(self.details[i], i)

    def findonedetail(self, code, OD, ID, thread, tab):
        d = []
        match code:
            case 405 | 413 | 418 | 610 | 611:
                d = DataManager.select_id_andor(code, OD, ID, thread, tab)
            case 557:
                d = DataManager.select_id_andwithoutor(code, OD, ID, thread)
            case 564 | 554 | 560: #502, 505, 510, 935, 241, 146, 501, 531, 552, 564, 533, 579
                d = DataManager.select_id_and(code, tab)
        return d[0][0]

    def findtwodetail(self, code, OD, ID, thread, tab):
        d = []
        match code:
            case 510:
                p = DataManager.select_id_andor(code, OD, ID, thread, tab)
                if not p:
                    code = 511
                    p = DataManager.select_id_andor(code, OD, ID, thread, tab)
                d = p
            case 502 | 552 | 531:
                p = DataManager.select_id_and(code, tab)
                if not p:
                    match code:
                        case 502:
                            code = 505
                        case 552:
                            code = 579
                        case 531:
                            code = 533
                    p = DataManager.select_id_and(code, tab)
                d = p
        return d[0][0]

    def finddetail(self, code, tab):
        d = DataManager.sql_query(f"SELECT id FROM Compon WHERE code LIKE '{code}%' AND thread_type='{tab}';")
        return d[0][0]

    def drawDB(self, TypeComp, OD=0, ID=0, thread="", tab="", count=1):
        details = []
        match TypeComp:
            case "Strike NC":
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G18-EN-0512';")
                details = [d[0][0]]
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G50-0512';")
                details.append(d[0][0])
                # запрос есть ли 510
                details.append(self.findtwodetail(510, OD, ID, thread, tab))
                for i in range(count):
                    if i + 1 == 1:
                        # запрос есть ли 502
                        details.append(self.findtwodetail(502, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                    if i + 1 > 1:
                        details.append(self.findonedetail(564, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                details.append(self.findonedetail(405, OD, ID, thread, tab))
                details.append(self.findonedetail(610, OD, ID, thread, tab))
                details.append(self.findonedetail(611, OD, ID, thread, tab))
                details.append(self.findonedetail(413, OD, ID, thread, tab))
            case "Strike RC":
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G18-EN-0512';")
                details = [d[0][0]]
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G50-0512';")
                details.append(d[0][0])
                # запрос есть ли 510
                details.append(self.findtwodetail(510, OD, ID, thread, tab))
                for i in range(count):
                    if i + 1 == 1:
                        details.append(self.findonedetail(557, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                    if i + 1 > 1:
                        details.append(self.findtwodetail(552, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                details.append(self.findonedetail(405, OD, ID, thread, tab))
                details.append(self.findonedetail(610, OD, ID, thread, tab))
                details.append(self.findonedetail(611, OD, ID, thread, tab))
                details.append(self.findonedetail(413, OD, ID, thread, tab))
            case "Strike RT":
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G18-EN-0512';")
                details = [d[0][0]]
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G50-0512';")
                details.append(d[0][0])
                # запрос есть ли 510
                details.append(self.findtwodetail(510, OD, ID, thread, tab))
                for i in range(count):
                    if i + 1 == 1:
                        details.append(self.findonedetail(557, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                    if i + 1 > 1:
                        details.append(self.findtwodetail(531, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                details.append(self.findonedetail(405, OD, ID, thread, tab))
                details.append(self.findonedetail(610, OD, ID, thread, tab))
                details.append(self.findonedetail(611, OD, ID, thread, tab))
                details.append(self.findonedetail(413, OD, ID, thread, tab))
            case "Spectr":
                details = [self.finddetail(501, tab)]
                details.append(self.finddetail(146, tab))
                details.append(self.finddetail(241, tab))
                details.append(self.finddetail(935, tab))
            case "Shuttle":
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G18-EN-0512';")
                details = [d[0][0]]
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G50-0512';")
                details.append(d[0][0])
                details.append(self.findtwodetail(510, OD, ID, thread, tab))
                for i in range(count):
                    if i + 1 == 1:
                        details.append(self.findonedetail(557, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                    if i + 1 > 1:
                        details.append(self.findonedetail(554, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                details.append(self.findonedetail(405, OD, ID, thread, tab))
                details.append(self.findonedetail(610, OD, ID, thread, tab))
                details.append(self.findonedetail(611, OD, ID, thread, tab))
                details.append(self.findonedetail(413, OD, ID, thread, tab))
            case "Solvtech":
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G18-EN-0512';")
                details = [d[0][0]]
                d = DataManager.sql_query("SELECT id FROM Compon WHERE code='G50-0512';")
                details.append(d[0][0])
                details.append(self.findtwodetail(510, OD, ID, thread, tab))
                for i in range(count):
                    if i + 1 == 1:
                        details.append(self.findonedetail(557, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                    if i + 1 > 1:
                        details.append(self.findonedetail(560, OD, ID, thread, tab))
                        details.append(self.findonedetail(418, OD, ID, thread, tab))
                details.append(self.findonedetail(405, OD, ID, thread, tab))
                details.append(self.findonedetail(610, OD, ID, thread, tab))
                details.append(self.findonedetail(611, OD, ID, thread, tab))
                details.append(self.findonedetail(413, OD, ID, thread, tab))
        self.details = details
        for i in range(len(self.details)):
            self.saveDetailsInProject(i+1, self.details[i])

    def createimg(self, i, inde):
        self.imgnumber = QLabel(self)
        self.imgnumber.setText(str(i[1]))
        self.imgnumber.setMaximumSize(110, 20)
        self.imgnumber.setFont(QFont("Arial", 12))
        self.imgnumber.setAlignment(Qt.AlignCenter)
        with Image.open(i[4]) as img_1:
            img_1.load()
        h = (img_1.height * 150) // img_1.width
        img = QPixmap(i[4]).scaled(150, h)  # href
        self.schemeLayout.label = ClickedLabel('Label')
        self.schemeLayout.label.setToolTip(i[2])  # name
        self.schemeLayout.label.setPixmap(paintIMGsmall(img))
        self.schemeLayout.label.enterEvent = self.onCursor
        self.schemeLayout.label.leaveEvent = self.offCursor
        self.girik = ""
        def giri():
            self.girik = inde
        self.schemeLayout.label.clicked.connect(lambda: giri())

        self.schemeLayout.addWidget(self.imgnumber)
        self.schemeLayout.addWidget(self.schemeLayout.label)
    def countsimilarpassport(self):
        if HoIn.CompositionType == "Spectr":
            return 4
        else:
            if HoIn.NumberOfStagesGRP == 1:
                return 9
            else:
                return 10

    def fill_tablecount(self):
        countrow_intablecount = self.countsimilarpassport()
        self.tablecount.setRowCount(countrow_intablecount)
        if self.cost > 0:
            self.lCost.show()
            self.refreshCost.show()
            self.inCost.show()
            self.tablecount.setColumnCount(7)
            for i in range(countrow_intablecount):
                self.tablecount.setItem(i, 0, QTableWidgetItem(str(i+1)))
                self.tablecount.setItem(i, 1, QTableWidgetItem(self.countandcost_details[i][1]))
                self.tablecount.setItem(i, 2, QTableWidgetItem(self.countandcost_details[i][2]))
                self.tablecount.setItem(i, 3, QTableWidgetItem(str(self.countandcost_details[i][3])))
                self.tablecount.setHorizontalHeaderLabels(
                    ["№", "Наименование", "Шифр", "Кол-во, шт", "ПЗ, тыс.руб", "Рентабельность, %", "Цена, тыс.руб"])
                costDetail = self.countandcost_details[i][5]
                if self.countandcost_details[i][3] > 1:
                    self.tablecount.setItem(i, 4, QTableWidgetItem(str(costDetail * self.countandcost_details[i][3]) + " (" + str(costDetail) + "/шт)"))
                else:
                    self.tablecount.setItem(i, 4, QTableWidgetItem(str(costDetail)))
                percent = self.countandcost_details[i][6]
                self.tablecount.setItem(i, 5, QTableWidgetItem(str(percent)))
                pr = round((100 + percent) / 100, 1)
                profitability = round(costDetail * pr, 1)
                if self.countandcost_details[i][3] > 1:
                    self.tablecount.setItem(i, 6, QTableWidgetItem(str(round(profitability * self.countandcost_details[i][3], 1)) + " (" + str(profitability) + "/шт)"))
                else:
                    self.tablecount.setItem(i, 6, QTableWidgetItem(str(profitability)))
            self.tablecount.resizeColumnsToContents()
            self._updateCost()
        else:
            self.tablecount.setColumnCount(4)
            for i in range(countrow_intablecount):
                self.tablecount.setItem(i, 0, QTableWidgetItem(str(i+1)))
                self.tablecount.setItem(i, 1, QTableWidgetItem(self.countandcost_details[i][1]))
                self.tablecount.setItem(i, 2, QTableWidgetItem(self.countandcost_details[i][2]))
                self.tablecount.setItem(i, 3, QTableWidgetItem(str(self.countandcost_details[i][3])))
                self.tablecount.setHorizontalHeaderLabels(["№", "Наименование", "Шифр", "Кол-во, шт"])
                self.tablecount.setColumnWidth(4, 0)
                self.tablecount.setColumnWidth(5, 0)
                self.tablecount.setColumnWidth(6, 0)
                self.tablecount.resizeColumnsToContents()


    # отрисовывает и заполняет таблицы
    def printProdTables(self):
        # table
        PrIn.TotalLength = 0
        self.table.setColumnCount(6)
        self.table.setRowCount(self.countDetails)
        self.table.setHorizontalHeaderLabels(
            ["№", "Наименование", "Шифр", "Наруж диам, мм", "Внут диам, мм", "Длина, мм"])
        for i in range(self.countDetails):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.details[i][1])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.details[i][2])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.details[i][3])))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.details[i][5])))
            self.table.setItem(i, 4, QTableWidgetItem(str(self.details[i][6])))
            self.table.setItem(i, 5, QTableWidgetItem(str(self.details[i][7])))
            PrIn.TotalLength += float(self.details[i][7])
        self.projectInfo.setItem(4, 1, QTableWidgetItem(str(PrIn.TotalLength) + ' мм'))
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # tablecount
        self.fill_tablecount()
        self.tablecount.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)


    # сохраняет детали в проект в бд
    def saveDetailsInProject(self, place, id_img):
        DataManager.sql_query(f"INSERT INTO Details (id_img, place, id_project) VALUES ({str(id_img)}, {str(place)}, {str(self.id)});")

    def values_table_in_tablecount(self, details):
        count_similar = []
        countandcost_details = []
        for j in details:
            c = 0
            for i in details:
                if i[2] == j[2]:
                    c += 1
                    if c > 1:
                        details.pop(details.index(i))
            count_similar += [c]
        num = 0
        for detail in details:
            num += 1
            countandcost_details += [(detail[0], detail[2], detail[3], count_similar[num - 1], detail[8], detail[9], detail[10], detail[1])]
        return countandcost_details

    # берет все детали проекта с их информацией и изображениями из бд
    def getImagesDetails(self):
        self.details = DataManager.selectseveraltable2(str(self.id))
        det = self.details.copy()
        self.countandcost_details = self.values_table_in_tablecount(det)



    # берет информацию по проекту из бд
    def getProjectFromDB(self):
        self.project = DataManager.select_project_id("company, field, well, bush, engineer, date, number_stages, type_comp, outer_diam, inner_diam, all_cost, date_cost, last_date, type, diam_open_barrel, reservoir_pres",
                                                     str(self.id))
        if self.project:
            DataManager.update('Project', 'last_date', str(datetime.now()), self.id)
            PrIn.Company = self.project[0][0]
            PrIn.Field = self.project[0][1]
            PrIn.Well = self.project[0][2]
            PrIn.Bush = self.project[0][3]
            engineer = DataManager.sql_query(f"SELECT name, contact FROM users WHERE id='{str(self.project[0][4])}';")
            if engineer:
                PrIn.Engineer = str(engineer[0][0])
                PrIn.ContactEngineer = str(engineer[0][1])
            else:
                self.messageboxerror("Возникли проблемы с соединением с базой данной")
            PrIn.Date = self.dateChange(self.project[0][5])
            HoIn.NumberOfStagesGRP = self.project[0][6]
            HoIn.CompositionType = self.project[0][7]
            if HoIn.CompositionType == "Spectr":
                self.countDetails = 4
            else:
                self.countDetails = 7+HoIn.NumberOfStagesGRP*2
            HoIn.DiameterExternal = self.project[0][8]
            HoIn.DiameterInterior = self.project[0][9]
            self.cost = self.project[0][10]
            self.inCost.setText(str(round(self.cost, 1)) + " руб")
            PrIn.DateFormationPrice = self.dateChange(self.project[0][11])
            PrIn.DateEdit = self.dateChange(self.project[0][12])
            PrIn.Type = self.project[0][13]
            HoIn.OpenHoleDiameter = self.project[0][14]
            HoIn.ReservoirPressure = self.project[0][15]
            self.tab = PrIn.Type
        else:
            self.messageboxerror("Возникли проблемы с соединением с базой данной")

    def dateChange(self, d):
        if d:
            d = d.split('-')
            return f'{d[2]}.{d[1]}.{d[0]}'

    # заполняет страницу данными
    def drawProject(self, PrIn = PrIn, HoIn = HoIn):
        """
        таблица общая информация
        """
        self.projectInfo.setItem(0, 1, QTableWidgetItem(PrIn.Company))
        self.projectInfo.setItem(0, 3, QTableWidgetItem(PrIn.Field))
        self.projectInfo.setItem(1, 1, QTableWidgetItem(PrIn.Well))
        self.projectInfo.setItem(1, 3, QTableWidgetItem(PrIn.Bush))
        self.projectInfo.setItem(2, 1, QTableWidgetItem(PrIn.Engineer))
        self.projectInfo.setItem(2, 3, QTableWidgetItem(PrIn.ContactEngineer))
        self.projectInfo.setItem(3, 1, QTableWidgetItem(PrIn.Date))
        self.projectInfo.setItem(3, 3, QTableWidgetItem(str(HoIn.NumberOfStagesGRP)))
        self.projectInfo.setItem(4, 3, QTableWidgetItem(PrIn.DateFormationPrice))
        """
        отрисовка изображений
        """
        self.getImagesDetails() #берем из бд детали
        self.drawsSheme() # отрисовывает картинки в блоке
        self.printProdTables() # отрисовывает и заполняет таблицу "информация по компоновке"
        self.lbl.show()
        self.lbl.setText(self.tab)
        self.getstatusesproject()

    def createInDBProject(self):
        dt = datetime.now()
        if DataManager.insert('Project', 'company', '0'):
            DataManager.insert('Statuses', 'status1, status2, status3, status4', "'False', 'False', 'False','False'")
            id_statuses = DataManager.sql_query("SELECT id FROM Statuses;")
            id_status = id_statuses[len(id_statuses)-1][0]
            self.id = DataManager.selectOne('Project', 'company', '0', 'id')
            if self.id:
                self.id = str(self.id[0][0])
                DataManager.sql_query(f"UPDATE Project SET all_cost='0' WHERE id={self.id};")
                DataManager.sql_query(f"UPDATE Project SET last_date='{dt}' WHERE id={self.id};")
                DataManager.sql_query(f"UPDATE Project SET id_status={id_status} WHERE id={self.id};")
                return True
            else:
                self.messageboxerror("Проблема с подключением к базе данных код 302")
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 303")


    # очищает страницу от данных проекта
    def CleanPage(self):
        for i in reversed(range(self.schemeLayout.count())):
            self.schemeLayout.itemAt(i).widget().setParent(None)
        self.FlagPrimaryCosts = False
        PrIn.TotalCost = 0
        PrIn.TotalLength = 0
        self.details = []

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
        for i in range (5):
            if (i < 5):
                self.projectInfo.setColumnWidth(i, int(self.projectInfo.width() // 4))
            self.projectInfo.setRowHeight(i, self.projectInfo.height() // 5)
        self.StatusBut.x1 = int(self.StatusBut.x0 * koefW)
            