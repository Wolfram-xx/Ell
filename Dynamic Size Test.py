from PyQt5 import QtCore, QtGui, QtWidgets

# from MplCanvas import MplCanvas                    # <<<--- установите свой виджет MplCanvas
from pyqtgraph import PlotWidget  # <<<--- это уберите


class Ui_Newton(object):
    def setupUi(self, Newton):
        Newton.setObjectName("Newton")
        Newton.setWindowModality(QtCore.Qt.WindowModal)
        Newton.resize(910, 850)
        self.centralwidget = QtWidgets.QWidget(Newton)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 20, 630, 570))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        #        self.graphicsView = MplCanvas()           # <<<--- установите свой виджет MplCanvas
        self.graphicsView = PlotWidget()  # <<<--- это уберите

        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QtCore.QRect(0, 610, 930, 200))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading |
                                   QtCore.Qt.AlignLeft |
                                   QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.a = QtWidgets.QLineEdit(self.groupBox)
        self.a.setGeometry(QtCore.QRect(490, 60, 180, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.a.setFont(font)
        self.a.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.a.setText("")
        self.a.setObjectName("a")
        self.b = QtWidgets.QLineEdit(self.groupBox)
        self.b.setGeometry(QtCore.QRect(720, 60, 180, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b.setFont(font)
        self.b.setText("")
        self.b.setObjectName("b")
        self.funcColor = QtWidgets.QComboBox(self.groupBox)
        self.funcColor.setGeometry(QtCore.QRect(30, 140, 160, 30))
        self.funcColor.setObjectName("funcColor")
        self.funcColor.addItem("")
        self.funcColor.addItem("")
        self.funcColor.addItem("")
        self.funcColor.addItem("")
        self.tangentColor = QtWidgets.QComboBox(self.groupBox)
        self.tangentColor.setGeometry(QtCore.QRect(260, 140, 160, 30))
        self.tangentColor.setObjectName("tangentColor")
        self.tangentColor.addItem("")
        self.tangentColor.addItem("")
        self.tangentColor.addItem("")
        self.tangentColor.addItem("")
        self.function = QtWidgets.QLineEdit(self.groupBox)
        self.function.setEnabled(True)
        self.function.setGeometry(QtCore.QRect(30, 60, 191, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.function.setFont(font)
        self.function.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.function.setWhatsThis("")
        self.function.setAccessibleName("")
        self.function.setAutoFillBackground(False)
        self.function.setInputMask("")
        self.function.setText("")
        self.function.setMaxLength(32767)
        self.function.setClearButtonEnabled(False)
        self.function.setObjectName("function")
        self.OK_NOK = QtWidgets.QDialogButtonBox(self.groupBox)
        self.OK_NOK.setGeometry(QtCore.QRect(720, 120, 180, 60))
        self.OK_NOK.setOrientation(QtCore.Qt.Vertical)
        self.OK_NOK.setStandardButtons(QtWidgets.QDialogButtonBox.Ok |
                                       QtWidgets.QDialogButtonBox.Reset)
        self.OK_NOK.setObjectName("OK_NOK")
        self.Inserta = QtWidgets.QLabel(self.groupBox)
        self.Inserta.setGeometry(QtCore.QRect(490, 30, 130, 20))
        self.Inserta.setObjectName("Inserta")
        self.Inserfunc = QtWidgets.QLabel(self.groupBox)
        self.Inserfunc.setGeometry(QtCore.QRect(30, 30, 250, 20))
        self.Inserfunc.setObjectName("Inserfunc")
        self.Insertb = QtWidgets.QLabel(self.groupBox)
        self.Insertb.setGeometry(QtCore.QRect(720, 30, 130, 20))

        # Текстовая строка интерпретируется как текст в формате Markdown.
        # Это значение перечисления было добавлено в Qt 5.14.
        # Раскомментируйте строку ниже, если у вас версия Qt 5.14 + .               !!!
        #        self.Insertb.setTextFormat(QtCore.Qt.MarkdownText)

        self.Insertb.setWordWrap(True)
        self.Insertb.setObjectName("Insertb")
        self.TangColor = QtWidgets.QLabel(self.groupBox)
        self.TangColor.setGeometry(QtCore.QRect(260, 110, 250, 20))
        self.TangColor.setObjectName("TangColor")
        self.FuncColor = QtWidgets.QLabel(self.groupBox)
        self.FuncColor.setGeometry(QtCore.QRect(30, 110, 250, 20))
        self.FuncColor.setObjectName("FuncColor")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(260, 30, 190, 20))
        self.label.setObjectName("label")
        self.variable = QtWidgets.QLineEdit(self.groupBox)
        self.variable.setGeometry(QtCore.QRect(260, 60, 200, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.variable.setFont(font)
        self.variable.setText("")
        self.variable.setObjectName("variable")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(490, 140, 150, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(490, 110, 160, 20))
        self.label_2.setObjectName("label_2")
        Newton.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Newton)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 910, 25))
        self.menubar.setObjectName("menubar")
        Newton.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Newton)
        self.statusbar.setObjectName("statusbar")
        Newton.setStatusBar(self.statusbar)

        self.retranslateUi(Newton)
        QtCore.QMetaObject.connectSlotsByName(Newton)

    def retranslateUi(self, Newton):
        _translate = QtCore.QCoreApplication.translate
        Newton.setWindowTitle(_translate("Newton", "Newton functions"))
        self.groupBox.setTitle(_translate("Newton",
                                          "Put data about your function here"))
        self.a.setPlaceholderText(_translate("Newton",
                                             "Put a value of [a, b] here"))
        self.b.setPlaceholderText(_translate("Newton",
                                             "Put b value of [a, b] here"))
        self.funcColor.setItemText(0, _translate("Newton", "blue"))
        self.funcColor.setItemText(1, _translate("Newton", "red"))
        self.funcColor.setItemText(2, _translate("Newton", "green"))
        self.funcColor.setItemText(3, _translate("Newton", "yellow"))
        self.tangentColor.setItemText(0, _translate("Newton", "red"))
        self.tangentColor.setItemText(1, _translate("Newton", "blue"))
        self.tangentColor.setItemText(2, _translate("Newton", "green"))
        self.tangentColor.setItemText(3, _translate("Newton", "yellow"))
        self.function.setPlaceholderText(_translate("Newton",
                                                    "Put your function here"))
        self.Inserta.setText(_translate("Newton",
                                        "<html><head/><body><p><span style=\""
                                        " font-size:10pt; font-weight:600;\">"
                                        "Insert </span><span style=\" "
                                        "font-size:10pt; font-weight:600; "
                                        "font-style:italic; text-decoration: "
                                        "underline;\">a</span></p>"
                                        "</body></html>"))
        self.Inserfunc.setText(_translate("Newton",
                                          "<html><head/><body>"
                                          "<p><span style=\" "
                                          "font-size:10pt; font-weight:600;\">"
                                          "Insert function</span>"
                                          "</p></body></html>"))
        self.Insertb.setText(_translate("Newton",
                                        "<html><head/><body><p><span style=\" "
                                        "font-size:10pt; "
                                        "font-weight:600;\">Insert "
                                        "</span>"
                                        "<span style=\" font-size:10pt; "
                                        "font-weight:600; font-style:italic; "
                                        "text-decoration: underline;\">b"
                                        "</span></p></body></html>"))
        self.TangColor.setText(_translate("Newton",
                                          "<html><head/>"
                                          "<body><p><span style=\" "
                                          "font-size:10pt; font-weight:600;\">"
                                          "Choose tangent color</span></p>"
                                          "</body></html>"))
        self.FuncColor.setText(_translate("Newton",
                                          "<html><head/><body><p>"
                                          "<span style=\" "
                                          "font-size:10pt; font-weight:600;"
                                          "\">Choose function color</span>"
                                          "</p></body></html>"))
        self.label.setText(_translate("Newton",
                                      "<html><head/><body><p>"
                                      "<span style=\" font-size:10pt;"
                                      " font-weight:600;\">"
                                      "Insert variable name</span>"
                                      "</p></body></html>"))
        self.variable.setPlaceholderText(_translate("Newton",
                                                    "Put your variable"
                                                    " name here"))
        self.comboBox.setItemText(0, _translate("Newton", "0.001"))
        self.comboBox.setItemText(1, _translate("Newton", "0.0001"))
        self.comboBox.setItemText(2, _translate("Newton", "0.00001"))
        self.comboBox.setItemText(3, _translate("Newton", "0.000001"))
        self.label_2.setText(_translate("Newton", "<html><head/><body><p>"
                                                  "<span style=\" "
                                                  "font-size:10pt; "
                                                  "font-weight:600;\">"
                                                  "Choose accuracy</span>"
                                                  "</p></body></html>"))


class MainWindow(QtWidgets.QMainWindow, Ui_Newton):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        gridgRoupBox = QtWidgets.QGridLayout(self.groupBox)
        gridgRoupBox.addWidget(self.Inserfunc, 0, 0)
        gridgRoupBox.addWidget(self.label, 0, 1)
        gridgRoupBox.addWidget(self.Inserta, 0, 2)
        gridgRoupBox.addWidget(self.Insertb, 0, 3)

        gridgRoupBox.addWidget(self.function, 1, 0)
        gridgRoupBox.addWidget(self.variable, 1, 1)
        gridgRoupBox.addWidget(self.a, 1, 2)
        gridgRoupBox.addWidget(self.b, 1, 3)

        gridgRoupBox.addWidget(self.FuncColor, 2, 0)
        gridgRoupBox.addWidget(self.TangColor, 2, 1)
        gridgRoupBox.addWidget(self.label_2, 2, 2, 1, 1)

        gridgRoupBox.addWidget(self.funcColor, 3, 0)
        gridgRoupBox.addWidget(self.tangentColor, 3, 1)
        gridgRoupBox.addWidget(self.comboBox, 3, 2)
        gridgRoupBox.addWidget(self.OK_NOK, 3, 3, alignment=QtCore.Qt.AlignCenter)

        self.grid = QtWidgets.QGridLayout(self.centralwidget)
        self.grid.addWidget(self.graphicsView, 0, 1, 1, 3)
        self.grid.addWidget(self.groupBox, 1, 0, 5, 5)

        #
        self.setTabOrder(self.function, self.variable)
        self.setTabOrder(self.variable, self.a)
        self.setTabOrder(self.a, self.b)
        self.setTabOrder(self.b, self.funcColor)
        self.setTabOrder(self.funcColor, self.tangentColor)
        self.setTabOrder(self.tangentColor, self.comboBox)
        self.setTabOrder(self.comboBox, self.OK_NOK)

        self.function.setFocus()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())