from os import name
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QWidget
from urllib.request import urlopen
import json

class loginScreen(QDialog):
    def __init__(self):
        super(loginScreen, self).__init__()
        loadUi("Login.ui", self)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        kScreen = KitchensScreen()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class KitchensScreen(QDialog):
    def __init__(self):
        super(KitchensScreen, self).__init__()
        loadUi("ListOfKitchens.ui", self)
        self.loadKitchens()
        self.kitchensList.itemDoubleClicked.connect(self.loadMenu)
        self.locationLabel.setText("Campus Center Market")

    def loadKitchens(self):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Kitchens"

        # store the response of URL
        response = urlopen(url)

        # storing the JSON response
        # # from url in data
        data_json = json.loads(response.read())
        self.kitchensList.addItems(data_json)

    def loadMenu(self):
        nameOfKitchen = self.kitchensList.currentItem().text()

        print(nameOfKitchen)

        # parameter for urlopen
        url = "http://127.0.0.1:8000/Kitchens/" + nameOfKitchen

        # store the response of URL
        response = urlopen(url)

        # storing the JSON response
        # # from url in data
        data_json = json.loads(response.read())

        print(data_json)

        self.menuList.clear()
        self.menuList.addItems(list(data_json.keys()))




#Setting up App
app = QApplication(sys.argv)
loginScreen = loginScreen()
widget = QStackedWidget()
widget.addWidget(loginScreen)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")