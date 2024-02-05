# подключение библиотек
import time
from datetime import datetime
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import threading

# подключение файлов
import DataManager
from PageAuthorization import PageAuthorization
from PageProjects import PageProjects
from PageInput1 import PageInput1
from PageInput2 import PageInput2
from PageOutput import PageOutput
from PageBigSheme import BigSheme
from PageNewDetail import PageNewDetail
import FileCreating
from Data import Data

# объявление глобальных переменных
PrIn = Data.ProjectInfo()
HoIn = Data.HoleInfo()


def validateInt(str):   # проверка строки на то, что введено число
    try:
        if (str != ""):
            int(str)
        if (str == ""):
            return False
        return True
    except BaseException:
        return False

def validateStr(str, count):    # проверка строки на то, что введена строка
    if (len(str) > count) or str == "":
        return False
    else:
        return True

def validateFloat(str): # проверка строки на то, что введено число с запятой
    try:
        if (str != ""):
            float(str)
        if (str == ""):
            return False
        return True
    except BaseException:
        return False


class EllCompletionApp(QWidget):
    resized = pyqtSignal()
    def __init__(self, parent=None):
        super(EllCompletionApp, self).__init__(parent)
        self.setWindowTitle("ELL COMPLETION APP")
        self.id_user = 1
        self.resize(1100, 550)
        self.setMinimumSize(1100, 550)
        self.oImage = QImage("icon/background.jpg").scaled(1920, 1080)
        self.SetBackgroundImg()

        """
        Объявление слоев
        """
        self.pAuthorization = PageAuthorization()
        self.pProjects = PageProjects()
        self.pInput1 = PageInput1()
        self.pInput2 = PageInput2()
        self.pOutput = PageOutput()
        self.pBigSheme = BigSheme()
        self.pNewDetail = PageNewDetail()
        self.setWindowIcon(QIcon('RimeraIcon.ico'))

        self.widget = QWidget()
        self.page = QStackedLayout()
        self.widget.setLayout(self.page)
        self.page.addWidget(self.pAuthorization)
        self.page.addWidget(self.pProjects)
        self.page.addWidget(self.pInput1)
        self.page.addWidget(self.pInput2)
        self.page.addWidget(self.pOutput)
        self.page.addWidget(self.pBigSheme)
        self.page.addWidget(self.pNewDetail)

        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.setLayout(layout)

        """
        Связи кнопок, событий и тд
        """
        # масштабирование экрана
        self.resized.connect(self.DynamicSize)
        # авторизация
        self.pAuthorization.butLogIn.clicked.connect(self.butBaseProj_Clicked)
        self.pProjects.butLeft.clicked.connect(self.LogOut)
        self.pAuthorization.inPass.editingFinished.connect(self.butBaseProj_Clicked)
        # меню проектов
        self.pProjects.tableProjects.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        self.pProjects.butOpenProj.clicked.connect(self.butOpenProj_Clicked)
        self.pProjects.butNewProj.clicked.connect(self.butNewProj_Clicked)
        self.pProjects.tableProjects.doubleClicked.connect(self.butOpenProj_Clicked)
        self.pProjects.butDelProj.clicked.connect(self.on_deleted_Clicked)
        # создание нового проекта
        self.pInput1.butLeft1.clicked.connect(self.butLeft1_Clicked)
        self.pInput1.butNext1.clicked.connect(self.butNext1_Clicked)
        self.pInput2.butLeft2.clicked.connect(self.butLeft2_Clicked)
        self.pInput2.butNext2.clicked.connect(self.butNext2_Clicked)
        self.pOutput.butLeftCreateProject.clicked.connect(self.LeftOpenProject)
        # вывод составленной компоновки
        self.pOutput.shemeWid.clicked.connect(self.openSheme)
        self.pBigSheme.BackBackBut.clicked.connect(self.closeSheme)
        self.pOutput.tablecount.selectionModel().selectionChanged.connect(self.pOutput.on_selectionChanged)
        self.pOutput.tablecount.cellChanged.connect(self.pOutput.cellchangedtable)
        self.pOutput.butLeft.clicked.connect(self.LeftOpenProject)
        self.pInput1.butLeft2.clicked.connect(self.butLeft2Input1_Clicked)
        # добавление нового оборудования
        self.pBigSheme.another.selectionModel().selectionChanged.connect(self.on_selectionChangedBS)
        self.pBigSheme.newcomp.clicked.connect(self.addnewcomp)
        self.pNewDetail.butLeft.clicked.connect(self.backBigSchema)
        self.pNewDetail.butCreate.clicked.connect(self.clickbutCreate)


    def dateChange(self, d):    # изменение даты в стандартную
        d = d.split('-')
        return f'{d[2]}.{d[1]}.{d[0]}'

    def SetBackgroundImg(self):
        sImage = self.oImage.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(self.oImage))
        self.setPalette(palette)

    """
    переход по страницам/окнам и сопутствующие им действия
    """
    def butBaseProj_Clicked(self):  # авторизация и проекты пользователя
        self.id_user = self.pAuthorization.LogIn()
        # сделать проверку на вводимые данные
        if self.id_user:
            self.showUserProjects()
            self.pProjects.getProjectsIdFromDB(str(self.id_user))
            self.page.setCurrentIndex(1)
            self.oImage = QImage("icon/background2.jpg").scaled(1920, 1080)
            self.SetBackgroundImg()
    def showUserProjects(self): # показ проектов у пользователя
        data = DataManager.select_user_id("name, access", self.id_user)
        if data:
            name = data[0][0]
            access = data[0][1]
            self.pProjects.lwelcomename.setText(name)
            self.pProjects.access = access
        else:
            self.messageboxerror("Возникли ошибка 002")

    def LogOut(self):   # выход из авторизации
        self.pProjects.butOpenProj.setIcon(QIcon("icon/OpenFileInactive.png"))
        self.pAuthorization.LogOut()
        self.pInput1.engineer_combo.clear()
        self.pProjects.tableProjects.clearSelection()
        self.page.setCurrentIndex(0)
        self.oImage = QImage("icon/background.jpg").scaled(1920, 1080)
        self.SetBackgroundImg()

    def addnewcomp(self):   # при добавлении новой компоновки переход на страницу
        self.page.setCurrentIndex(6)

    def backBigSchema(self):    # уход со страницы большого вида
        self.page.setCurrentIndex(5)
        self.pNewDetail.cleanPage()

    def clickbutCreate(self):   # добавление нового оборудования
        self.pNewDetail.clickbutCreate(self.pOutput.tab)
        if self.pNewDetail.flagAboutCreateNewDetail:
            self.pBigSheme.id_detail = self.pOutput.details[self.pBigSheme.index][0]
            self.pBigSheme.searchAnotherDetails(self.pOutput.details[self.pBigSheme.index][3])
            self.backBigSchema()



    def on_deleted_Clicked(self):   # удаление проекта
        id = self.pProjects.projects[self.pProjects.ind][0]
        self.dlg = QMessageBox()
        self.dlg.addButton("Да", QMessageBox.AcceptRole)
        self.dlg.addButton("Назад", QMessageBox.AcceptRole)
        self.dlg.setWindowTitle("Удаление")
        self.dlg.setInformativeText("Удалить выбранный проект?")
        self.dlg.show()
        self.dlg.exec()
        if self.dlg.clickedButton().text() == "Да":
            DataManager.delete('Project', str(id))
        else:
            pass
        self.pProjects.getProjectsIdFromDB(str(self.id_user))

    def on_selectionChanged(self, selected):    # выбор проекта
        for i in selected.indexes():
            self.pProjects.ind = int(i.row())
            self.pProjects.butOpenProj.setIcon(QIcon("icon/OpenFile.png"))
            self.pOutput.id = int(self.pProjects.projects[self.pProjects.ind][0])
            self.pBigSheme.id_project = int(self.pOutput.id)

    def on_selectionChangedBS(self, selected):  # выбор оборудования для замены
        for i in selected.indexes():
            ind = i.row()
            self.dlg = QMessageBox()
            self.dlg.addButton("Да", QMessageBox.AcceptRole)
            self.dlg.addButton("Отмена", QMessageBox.AcceptRole)
            self.dlg.setWindowTitle("Поменять")
            self.dlg.setInformativeText("Поменять на выбранное оборудование?")
            self.dlg.show()
            self.dlg.exec()
            if self.dlg.clickedButton().text() == "Да":
                self.pBigSheme.changePlaceDetails(ind)
                self.pOutput.getImagesDetails()
                self.pOutput.details.reverse()
                self.pOutput.printProdTables()
                self.pOutput.tablecount.resizeColumnsToContents()
                self.pBigSheme.details = self.pOutput.details
                self.pBigSheme.updatePage()
            else:
                self.pBigSheme.another.clearSelection()
                pass


    def create_list_engineer(self): # создание списка менеджеров по подбору
        users = DataManager.select_users_where("name, id", "access!='all'")
        if users:
            for user in users:
                self.pInput1.engineer_combo.addItem(user[0])
            self.pInput1._onEngineerActivated(users[0][0])
        else:
            self.messageboxerror("Возникла проблемa 003")
        return users

    def write_fields_engineer(self, access, users): # заполнение контакта
        if access == "part":
            contact = DataManager.select_user_id("contact", str(self.id_user))
            for i in range(len(users)):
                if users[i][1] == self.id_user:
                    self.pInput1.engineer_combo.setCurrentIndex(i)
                else:
                    self.pInput1.engineer_combo.setCurrentIndex(0)
            if contact:
                self.pInput1.inPhoneNumber.setText(contact[0][0])
            else:
                self.messageboxerror("Возникли проблемы с соединением с базой данной")
        else:
            self.pInput1.engineer_combo.setCurrentIndex(0)


    def butNewProj_Clicked(self):   # переход на первую страницу заполнения данных
        if self.pOutput.createInDBProject():
            users = self.create_list_engineer()
            self.write_fields_engineer(self.pProjects.access, users)
            self.pInput1.lTitle.setText("Создание нового проекта")
            self.pInput1.butLeft2.hide()
            self.pInput1.butLeft1.show()
            self.page.setCurrentIndex(2)
            self.oImage = QImage("icon/background3.jpg").scaled(1920, 1080)
            self.SetBackgroundImg()
    def butLeft1_Clicked(self): # покинуть первую страницу заполнения данных
        self.pProjects.tableProjects.clearSelection()
        self.page.setCurrentIndex(1)
        self.oImage = QImage("icon/background2.jpg").scaled(1920, 1080)
        self.SetBackgroundImg()
        # очистить первую страницу ввода данных
        self.pInput1.inCompany.clear()
        self.pInput1.inBush.clear()
        self.pInput1.inWell.clear()
        self.pInput1.inField.clear()
        # очистить вторую страницу ввода данных
        self.pInput2.inInnerDiam.clear()
        self.pInput2.inOuterDiam.clear()

    def butLeft2Input1_Clicked(self):   # покинуть вторую страницу заполнения данных
        self.page.setCurrentIndex(4)

    def updatePrIn(self):   # обновление данных в бд
        if ((DataManager.update('Project', 'company', PrIn.Company, self.id)) and
            (DataManager.update('Project', 'field', PrIn.Field, self.id)) and
            (DataManager.update('Project', 'bush', PrIn.Bush, self.id)) and
            (DataManager.update('Project', 'well', PrIn.Well, self.id)) and
            (DataManager.update('Project', 'date', PrIn.Date, self.id)) and
            (DataManager.update('Project', 'engineer', PrIn.Engineer, self.id))):
            return True
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 1011")

    def butNext1_Clicked(self): # проверка и сохранение данных первой страницы заполнения данных
        if not (validateStr(self.pInput1.inCompany.text(), 30)
                and validateStr(self.pInput1.inField.text(), 30)
                and validateStr(self.pInput1.inPhoneNumber.text(), 100)
                and validateStr(self.pInput1.inBush.text(), 30)
                and validateStr(self.pInput1.inWell.text(), 30)):
            self.messageboxerror("Поля пусты или переполнены(не более 30 знаков)")
            return
        PrIn.Company = self.pInput1.inCompany.text()
        PrIn.Field = self.pInput1.inField.text()
        selectDate = self.pInput1.inData.date()
        PrIn.Date = selectDate.toString(Qt.ISODate)
        PrIn.Bush = self.pInput1.inBush.text()
        PrIn.Well = self.pInput1.inWell.text()
        PrIn.ContactEngineer = self.pInput1.inPhoneNumber.text()
        self.id = self.pOutput.id
        engineer = DataManager.select_users_where("id", "name='" + self.pInput1.engineer_combo.currentText() + "'")
        if engineer:
            PrIn.Engineer = str(engineer[0][0])
            self.updatePrIn()
            self.page.setCurrentIndex(3)
        else:
            self.messageboxerror("Проблема с подключением к базе данных код 1012")


    def butLeft2_Clicked(self): # покинуть первую страницу заполнения данных
        self.page.setCurrentIndex(2)

    def messageboxerror(self, text):    # сообщение об ошибке
        msg = QMessageBox.critical(self, "Ошибка ", text, QMessageBox.Ok)
        return

    def findcheck(self, arr, det):  # проверка кода оборудования
        if len(det) == 3:
            for i in range(len(arr)):
                if arr[i][0] == det:
                    return True
            return False
        if len(det) == 2:
            flag = 0
            for d in det:
                for i in range(len(arr)):
                    if arr[i][0] == d:
                        flag += 1
                        break
            if flag == 0:
                return False
            return True

    def checkData(self, TypeComp, ThreadType, OD, ID, thread):  # проверка, можно ли составить схему
        finddetail = []
        p = []
        if OD < ID or OD == ID:
            return False
        match TypeComp:
            case "Strike NC":
                p = DataManager.selectdistinctsubctringcode(
                    f"(thread_type='{ThreadType}' OR thread_type='Strike {OD}-{ID} {thread}')")
                finddetail = [["510", "511"], ["502", "505"], "418", "564", "405", "610", "611", "413"]
            case "Strike RC":
                p = DataManager.selectdistinctsubctringcode(
                    f"(thread_type='{ThreadType}' OR thread_type='Strike {OD}-{ID} {thread}')")
                finddetail = [["510", "511"], "557", ["552", "579"], "418", "405", "610", "611", "413"]
            case "Strike RT":
                p = DataManager.selectdistinctsubctringcode(
                    f"(thread_type='{ThreadType}' OR thread_type='Strike {OD}-{ID} {thread}')")
                finddetail = [["510", "511"], "557", "418", ["531", "533"], "405", "610", "611", "413"]
            case "Spectr":
                p = DataManager.selectdistinctsubctringcode(f"thread_type='{ThreadType}'")
                finddetail = ["501", "146", "241", "935"]
            case "Solvtech":
                p = DataManager.selectdistinctsubctringcode(
                    f"(thread_type='{TypeComp}' OR"
                    f" thread_type='Strike {OD}-{ID} {thread}' OR"
                    f" thread_type='Strike RC {OD}-{ID} {thread}' OR"
                    f" thread_type='Strike RT {OD}-{ID} {thread}')")
                finddetail = [["510", "511"], "557", "418", "560", "405", "610", "611", "413"]
            case "Shuttle":
                p = DataManager.selectdistinctsubctringcode(
                    f"(thread_type='{TypeComp}' OR"
                    f" thread_type='Strike {OD}-{ID} {thread}' OR"
                    f" thread_type='Strike RC {OD}-{ID} {thread}' OR"
                    f" thread_type='Strike RT {OD}-{ID} {thread}')")
                finddetail = [["510", "511"], "557", "418", "554", "405", "610", "611", "413"]
        for det in finddetail:
            f = self.findcheck(p, det)
            if not f:
                return False
        return True


    def saveHoIn(self): # сохранение в глобальную переменную с полей ввода
        if self.pInput2.inDownhole11.text() != "":
            HoIn.WellBottomProjMD = int(self.pInput2.inDownhole11.text())
        if self.pInput2.inDownhole12.text() != "":
            HoIn.WellBottomProjTVD = int(self.pInput2.inDownhole12.text())
        if self.pInput2.inDownhole21.text() != "":
            HoIn.WellBottomFactMD = int(self.pInput2.inDownhole21.text())
        if self.pInput2.inDownhole11.text() != "":
            HoIn.WellBottomFactTVD = int(self.pInput2.inDownhole22.text())
        if self.pInput2.inDiamOpenBarrel.text() != "":
            HoIn.OpenHoleDiameter = int(self.pInput2.inDiamOpenBarrel.text())
        if self.pInput2.inOffsetFromVert.text() != "":
            HoIn.OffsetVertical = int(self.pInput2.inOffsetFromVert.text())
        if self.pInput2.inLenBarrel.text() != "":
            HoIn.OpenHoleLenght = int(self.pInput2.inLenBarrel.text())
        if self.pInput2.inCorner.text() != "":
            HoIn.MaxAngle = int(self.pInput2.inCorner.text())
        if self.pInput2.inInterval.text() != "":
            HoIn.MaxAngleInterval = int(self.pInput2.inInterval.text())
        if self.pInput2.inTypeWell.currentText() != "":
            HoIn.HoleType = self.pInput2.inTypeWell.currentText()
        if self.pInput2.inReservoirPres.text() != "":
            HoIn.ReservoirPressure = int(self.pInput2.inReservoirPres.text())
        if self.pInput2.inWellHeadPres.text() != "":
            HoIn.WellheadPressure = int(self.pInput2.inWellHeadPres.text())
        if self.pInput2.inDesInterShank.text() != "":
            HoIn.LinerRunningInterval = self.pInput2.inDesInterShank.text()
        if self.pInput2.inDescentDepth.text() != "":
            HoIn.DescentDepth = int(self.pInput2.inDescentDepth.text())
        if self.pInput2.inDepthCCODE.text() != "":
            HoIn.CKODdepth = int(self.pInput2.inDepthCCODE.text())


    def updateHoIn(self):   # обновление данных в бд
        DataManager.update('Project', 'type_well', HoIn.HoleType, self.id)
        DataManager.update('Project', 'downhole11', HoIn.WellBottomProjMD, self.id)
        DataManager.update('Project', 'downhole12', HoIn.WellBottomProjTVD, self.id)
        DataManager.update('Project', 'downhole21', HoIn.WellBottomFactMD, self.id)
        DataManager.update('Project', 'downhole22', HoIn.WellBottomFactTVD, self.id)
        DataManager.update('Project', 'diam_open_barrel', HoIn.OpenHoleDiameter, self.id)
        DataManager.update('Project', 'offset_from_vert', HoIn.OffsetVertical, self.id)
        DataManager.update('Project', 'len_barrel', HoIn.OpenHoleLenght, self.id)
        DataManager.update('Project', 'corner', HoIn.MaxAngle, self.id)
        DataManager.update('Project', 'interval', HoIn.MaxAngleInterval, self.id)
        DataManager.update('Project', 'reservoir_pres', HoIn.ReservoirPressure, self.id)
        DataManager.update('Project', 'Well_head_pres', HoIn.WellheadPressure, self.id)
        DataManager.update('Project', 'des_inter_shank', HoIn.LinerRunningInterval, self.id)
        DataManager.update('Project', 'descent_depth', HoIn.DescentDepth, self.id)
        DataManager.update('Project', 'depth_ccode', HoIn.CKODdepth, self.id)
        DataManager.update('Project', 'outer_diam', str(HoIn.DiameterExternal), self.id)
        DataManager.update('Project', 'inner_diam', str(HoIn.DiameterInterior), self.id)
        DataManager.update('Project', 'number_stages', str(HoIn.NumberOfStagesGRP), self.id)
        DataManager.update('Project', 'type_comp', str(HoIn.CompositionType), self.id)

    def createtab(self, CompType, OD=0, ID=0, thread=""):   # составление названия компоновки
        match CompType:
            case "Strike NC" | "Strike RC" | "Strike RT":
                return f"{CompType} {OD}-{ID} {thread}"
            case "Spectr":
                return f"{CompType} {ID}"
            case _:
                return CompType

    def butNext2_Clicked(self): # проверка вводимых данных и составление схемы
        if not (validateFloat(self.pInput2.inOuterDiam.text())
                and validateFloat(self.pInput2.inInnerDiam.text())
                and validateInt(self.pInput2.inNumberStages.text())):
            self.messageboxerror("Поля пусты или имеют недопустимые значения")
            return
        HoIn.NumberOfStagesGRP = int(self.pInput2.inNumberStages.text())
        try:
            if HoIn.NumberOfStagesGRP > 70:
                self.messageboxerror("Введенное кол-во стадий превышено")
                return
            if HoIn.NumberOfStagesGRP == 0:
                self.messageboxerror("Кол-во стадий не может быть равно нулю")
                return
        except BaseException:
            self.messageboxerror("Неверное значение")
            return
        self.saveHoIn()
        HoIn.DiameterExternal = round(float(self.pInput2.inOuterDiam.text()))
        HoIn.DiameterInterior = round(float(self.pInput2.inInnerDiam.text()))
        HoIn.CompositionType = self.pInput2.compon_combo.currentText()
        thrtype = self.pInput2.thread_combo.currentText()
        tab = self.createtab(HoIn.CompositionType, HoIn.DiameterExternal, HoIn.DiameterInterior, thrtype)
        if self.checkData(HoIn.CompositionType, tab, HoIn.DiameterExternal, HoIn.DiameterInterior, thrtype):
            match HoIn.CompositionType:
                case "Spectr":
                    self.pOutput.countDetails = 4
                case _:
                    self.pOutput.countDetails = HoIn.NumberOfStagesGRP * 2 + 7
            # отправление данных в базу данных
            DataManager.update('Project', 'type', str(tab), self.id)
            self.updateHoIn()
            self.pOutput.getProjectFromDB()
            self.pOutput.drawDB(HoIn.CompositionType, HoIn.DiameterExternal, HoIn.DiameterInterior, thrtype, tab, HoIn.NumberOfStagesGRP)
            self.pOutput.drawProject()
            self.pOutput.butLeft.hide()
            self.pOutput.butInput.hide()
            self.pOutput.butLeftCreateProject.show()
            self.page.setCurrentIndex(4)
        else:
            self.messageboxerror("Такие параметры недоступны")

    def butOpenProj_Clicked(self):  # открытие проекта
        self.setCursor(QCursor(Qt.BusyCursor))
        if (self.pProjects.ind != -1):
            self.pOutput.butLeft.show()
            self.pOutput.butInput.show()
            self.pOutput.butLeftCreateProject.hide()
            self.pOutput.getProjectFromDB()
            self.pOutput.drawProject()
            self.pBigSheme.tab = self.pOutput.tab
            self.page.setCurrentIndex(4)
            self.oImage = QImage("icon/background3.jpg").scaled(1920, 1080)
            self.SetBackgroundImg()
        else:
            QMessageBox.critical(self, "Ошибка", "Проект не выбран", QMessageBox.Ok)
            return
        self.setCursor(QCursor(Qt.ArrowCursor))

    def LeftOpenProject(self):  # покинуть(закрыть) открытый проект
        self.pInput1.clean_page()
        self.pInput2.clean_page()
        self.pProjects.getProjectsIdFromDB(str(self.id_user))
        self.pOutput.lCost.hide()
        self.pOutput.refreshCost.hide()
        self.pOutput.inCost.hide()
        self.pOutput.butLeftCreateProject.hide()
        self.pOutput.CleanPage()
        self.pProjects.tableProjects.clearSelection()
        self.page.setCurrentIndex(1)
        self.oImage = QImage("icon/background2.jpg").scaled(1920, 1080)
        self.SetBackgroundImg()

    def DoubleClickProjectInfo(self):   # редактирование проекта
        self.pOutput.CleanPage()
        self.pInput1.lTitle.setText("Редактирование проекта")
        self.pInput1.butLeft2.show()
        self.page.setCurrentIndex(2)

    """
    подробный вид оборудования
    """
    def openSheme(self):    # открытие подробного вида
        self.page.setCurrentIndex(5)
        self.pBigSheme.details = self.pOutput.details
        self.pBigSheme.index = self.pOutput.girik
        self.pBigSheme.setImage(self.pOutput.details)
    def closeSheme(self):   # закрытие подробного вида
        self.page.setCurrentIndex(4)

    def searchImageonSheme(self):
        try:
            if (len(self.pBigSheme.details) != 0):
                self.pBigSheme.index = int(self.pBigSheme.Number.text()) - 1
                self.pBigSheme.setImage(self.pOutput.details)
        except:
            pass

    def ClearLayout(self):
        self.pOutput.images = []

    def DynamicSize(self):
        koefW = self.size().width() / 1100
        koefH = self.size().height() / 550
        self.pAuthorization.DynamicSize(koefW, koefH)
        self.pProjects.DynamicSize(koefW, koefH)
        self.pInput1.DynamicSize(koefW, koefH)
        self.pInput2.DynamicSize(koefW, koefH)
        self.pOutput.DynamicSize(koefW, koefH)
        self.pBigSheme.DynamicSize(koefW, koefH)
        self.pNewDetail.DynamicSize(koefW, koefH)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(EllCompletionApp, self).resizeEvent(event)


def exitSoftAndDb(app):
    app.exec_()
    DataManager.sql_connection_close()

def start(app):
    win = EllCompletionApp()
    win.show()
    sys.exit(exitSoftAndDb(app))

class LoadingScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(QSize(600, 600))
        QSplashScreen.__init__(self, pixmap)
        self.setPixmap(QPixmap("icon/LoadScreen.jpg"))

def load(app):
    progressbar_value = 30
    splash = LoadingScreen()
    progressbar = QProgressBar(splash)
    progressbar.setMaximum(progressbar_value)
    progressbar.setGeometry(50, 500, 500, 50)
    progressbar.setTextVisible(False)
    splash.show()
    for i in range(progressbar_value):
        progressbar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load(app)
    start(app)

