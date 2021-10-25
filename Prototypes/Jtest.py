# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Jtest.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen
import json


# parameter for urlopen
url = "http://127.0.0.1:8000/Kitchens"

# store the response of URL
response = urlopen(url)

# storing the JSON response
# from url in data
data_json = json.loads(response.read())

class secondWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 500, 600)
        
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Return to menu")
        self.button1.resize(500, 100)
        self.button1.setStyleSheet("background-color: orange;font-size:18px;font-family:Times New Roman;");

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(843, 622)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.frame)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(40)
        font.setBold(False)
        font.setWeight(50)
        self.listWidget.setFont(font)
        self.listWidget.setMouseTracking(False)
        self.listWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listWidget.setLineWidth(0)
        self.listWidget.setMidLineWidth(0)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setWordWrap(False)
        self.listWidget.setObjectName("listWidget")
        # item = QtWidgets.QListWidgetItem()
        # item.setTextAlignment(QtCore.Qt.AlignCenter)
        # brush = QtGui.QBrush(QtGui.QColor(169, 255, 173))
        # brush.setStyle(QtCore.Qt.SolidPattern)
        # item.setBackground(brush)
        # self.listWidget.addItem(item)
        # item = QtWidgets.QListWidgetItem()
        # item.setTextAlignment(QtCore.Qt.AlignCenter)
        # brush = QtGui.QBrush(QtGui.QColor(169, 255, 173))
        # brush.setStyle(QtCore.Qt.SolidPattern)
        # item.setBackground(brush)
        # self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 843, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, data_json)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.listWidget.itemDoubleClicked.connect(self.secondWindow)


    def retranslateUi(self, MainWindow, listOfKitchens):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        # item = self.listWidget.item(0)
        # item.setText(_translate("MainWindow", "Sushi"))
        # item = self.listWidget.item(1)
        # item.setText(_translate("MainWindow", "Market"))
        self.listWidget.addItems(listOfKitchens)
        self.listWidget.setSortingEnabled(__sortingEnabled)

    def secondWindow(self):
        self.w = secondWindow()
        self.w.show()
        #self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
