from os import name
import sys
import requests
sys.path.append('../')
from DeskFoodModels.DeskFoodLib import Kitchen, Menu, Item
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QDialog, QApplication, QStackedWidget, QWidget
from urllib.request import urlopen
import json

#--------------------Login Window--------------------
class loginScreen(QDialog):
    def __init__(self):
        super(loginScreen, self).__init__()
        loadUi("Login.ui", self)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        kScreen = kitchenMenu()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Select Option Window--------------------
class kitchenMenu(QDialog):
    def __init__(self):
        super(kitchenMenu, self).__init__()
        loadUi("KitchenMenu.ui", self)
        self.AddItemBTN.clicked.connect(self.addItem)
        self.viewKitchensBTN.clicked.connect(self.viewKitchens)

    def addItem(self):
        kScreen = kitchenAddItem()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def viewKitchens(self):
        kScreen = KitchensScreen()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Kitchens Add Item Window--------------------
class kitchenAddItem(QDialog):
    def __init__(self):
        super(kitchenAddItem, self).__init__()
        loadUi("KitchenAddItem.ui", self)
        self.returnBTN.clicked.connect(self.goBack)
        self.freshensCheck.clicked.connect(self.unclickF)
        self.deliCheck.clicked.connect(self.unclickD)
        self.pizzaCheck.clicked.connect(self.unclickP)
        self.burgerCheck.clicked.connect(self.unclickB)
        self.marketCheck.clicked.connect(self.unclickM)
        self.finishBTN.clicked.connect(self.finish)

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
    def unclickF(self):
        self.freshensCheck.setChecked(1)
        self.deliCheck.setChecked(0)
        self.pizzaCheck.setChecked(0)
        self.burgerCheck.setChecked(0)
        self.marketCheck.setChecked(0)
        
    def unclickD(self):
        self.freshensCheck.setChecked(0)
        self.deliCheck.setChecked(1)
        self.pizzaCheck.setChecked(0)
        self.burgerCheck.setChecked(0)
        self.marketCheck.setChecked(0)
        
    def unclickP(self):
        self.freshensCheck.setChecked(0)
        self.deliCheck.setChecked(0)
        self.pizzaCheck.setChecked(1)
        self.burgerCheck.setChecked(0)
        self.marketCheck.setChecked(0)
        
    def unclickB(self):
        self.freshensCheck.setChecked(0)
        self.deliCheck.setChecked(0)
        self.pizzaCheck.setChecked(0)
        self.burgerCheck.setChecked(1)
        self.marketCheck.setChecked(0)
        
    def unclickM(self):
        self.freshensCheck.setChecked(0)
        self.deliCheck.setChecked(0)
        self.pizzaCheck.setChecked(0)
        self.burgerCheck.setChecked(0)
        self.marketCheck.setChecked(1)
        
    def finish(self):
        if(len(self.textName.toPlainText()) > 0):
            if(len(self.textCost.toPlainText()) > 0):
                if((self.freshensCheck.checkState()) or (self.deliCheck.checkState()) or (self.pizzaCheck.checkState()) or (self.burgerCheck.checkState()) or self.marketCheck.checkState()):
                    available = False
                    if(self.checkBox.checkState()): available = True
                    if(self.freshensCheck.checkState()): mykitchen = "Freshens"
                    if(self.deliCheck.checkState()): mykitchen = "Deli"
                    if(self.pizzaCheck.checkState()): mykitchen = "Pizza"
                    if(self.burgerCheck.checkState()): mykitchen = "Burgers"
                    if(self.marketCheck.checkState()): mykitchen = "Market"
                    item = Item(name = self.textName.toPlainText(), price = self.textCost.toPlainText(), available = available)
                    r = requests.put("http://localhost:8000/AddToMenu/" + mykitchen, item.json())
                    self.textName.setText("")
                    self.textCost.setText("")
                    self.checkBox.setChecked(0)
                    self.freshensCheck.setChecked(0)
                    self.deliCheck.setChecked(0)
                    self.pizzaCheck.setChecked(0)
                    self.burgerCheck.setChecked(0)
                    self.marketCheck.setChecked(0)

#--------------------Kitchens and Menu Window--------------------
class KitchensScreen(QDialog):
    def __init__(self):
        super(KitchensScreen, self).__init__()
        loadUi("ListOfKitchens.ui", self)
        self.loadKitchens()
        self.kitchensList.itemDoubleClicked.connect(self.loadMenu)
        self.locationLabel.setText("Campus Center Market")
        self.returnBTN.clicked.connect(self.goBack)

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

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

#--------------------MAIN--------------------
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