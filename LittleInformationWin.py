import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.Qt import QFontDatabase
from PyQt5.QtGui import QFont
import sys
class InformationWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите дополнительную информацию")
        fontIdR = QFontDatabase.addApplicationFont("Fonts/Circe-Regular.ttf")
        Circle_Regular = QFontDatabase.applicationFontFamilies(fontIdR)[0]


        self.ServiceNameL = QLabel(self)
        self.ServiceNameL.setText("Сервисный центр")
        self.ServiceNameL.move(0, 20)
        self.ServiceName = QLineEdit(self)
        self.ServiceName.resize(150, 50)
        self.ServiceName.move(200, 0)

        self.ServiceNameL = QLabel(self)
        self.ServiceNameL.setText("Представитель")
        self.ServiceNameL.move(0, 80)
        self.ServiceMan = QLineEdit(self)
        self.ServiceMan.resize(150, 50)
        self.ServiceMan.move(200, 60)

        self.ServiceNameL = QLabel(self)
        self.ServiceNameL.setText("Телефон серв. центра")
        self.ServiceNameL.move(0, 140)
        self.ServiceNum = QLineEdit(self)
        self.ServiceNum.resize(150, 50)
        self.ServiceNum.move(200, 120)

        self.ServiceNameL = QLabel(self)
        self.ServiceNameL.setText("Стол ротора")
        self.ServiceNameL.move(0, 200)
        self.TableRotor = QLineEdit(self)
        self.TableRotor.resize(150, 50)
        self.TableRotor.move(200, 180)

        self.ServiceNameL = QLabel(self)
        self.ServiceNameL.setText("Буровой раствор")
        self.ServiceNameL.move(0, 260)
        self.drillingFluid = QLineEdit(self)
        self.drillingFluid.resize(150, 50)
        self.drillingFluid.move(200, 240)

        self.ButSave = QPushButton(self)
        self.ButSave.resize(350, 70)
        self.ButSave.move(0, 300)
        self.ButSave.setText("Сохранить как...")
        self.ButSave.setStyleSheet("QPushButton {background-color: rgb(235,86,79); color: White; border-radius: 1px;}"
                           "QPushButton:pressed {background-color:rgb(251,114,107) ; }")


        for i in self.children():
            try:
                i.setFont(QFont(Circle_Regular, 12))
            except:
                pass
        self.ButSave.setFont(QFont(Circle_Regular, 18))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = InformationWin()
    win.show()
    sys.exit(app.exec_())