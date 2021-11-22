from os import name
import sys
from pyasn1_modules.rfc2459 import Name
import requests
sys.path.append('../')
from DeskFoodModels.DeskFoodLib import Kitchen, Menu, Item
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QApplication, QListWidget, QMenu, QPushButton, QStackedWidget, QTextBrowser, QWidget
from urllib.request import urlopen
import json
from DeskFoodModels import firebaseAuth

#--------------------Login Window--------------------
class loginScreen(QDialog):
    def __init__(self):
        super(loginScreen, self).__init__()
        loadUi("Login.ui", self)
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    def login(self):
        self.username = self.emailEdit.text()
        self.password = self.passwordEdit.text()
        self.user = firebaseAuth.login(self.username, self.password)

        if self.user:
            if(self.username == "admin@admin.com"):
                self.acceptadmin()
            else:
                self.accept()
        else:
            self.emailEdit.setText("")
            self.passwordEdit.setText("")
            self.emailEdit.setFocus()
            #self.errorLabel.setText("Invalid username or password")

    def register(self):
        kScreen = registerScreen()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def accept(self):
        kScreen = customerORRunner()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def acceptadmin(self):
        kScreen = kitchenMenu()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Register Window--------------------
class registerScreen(QDialog):
    def __init__(self):
        super(registerScreen, self).__init__()
        loadUi("SignUp.ui", self)
        self.registerButton.clicked.connect(self.register)
        self.registerButton.setEnabled(False)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordConfirmEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.termsAndConditionsRadioButton.toggled.connect(self.enableRegisterButton)

    def register(self):
        self.username = self.userNameEdit.text()
        self.password = self.passwordEdit.text()
        self.passwordConfirm = self.passwordConfirmEdit.text()
        self.email = self.emailEdit.text()

        if self.username != "" and self.password != "" and self.passwordConfirm != "":
            if self.password == self.passwordConfirm:
                self.user = firebaseAuth.register(self.email, self.password, self.username)
                if self.user:
                    self.accept()
                
        self.passwordEdit.setText("")
        self.passwordConfirmEdit.setText("")
        self.userNameEdit.setFocus()
        #self.errorLabel.setText("Invalid username or password")

    def enableRegisterButton(self):
        if self.termsAndConditionsRadioButton.isChecked():
            self.registerButton.setEnabled(True)
        else:
            self.registerButton.setEnabled(False)

    def accept(self):
        kScreen = customerORRunner()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


#--------------------Customer or Runner Window---------------
class customerORRunner(QDialog):
    def __init__(self):
        super(customerORRunner, self).__init__()
        loadUi("customerORrunner.ui", self)
        self.customerBTN.clicked.connect(self.customer)
        self.runnerBTN.clicked.connect(self.runner)
        

    def customer(self):
        kScreen = orderWindow()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def runner(self):
        kScreen = kitchenMenu()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Order Window----------------------------
class orderWindow(QDialog):
    #TODO: Fix number format by rounding it to 2 decimal places
    def __init__(self):
        super(orderWindow, self).__init__()
        loadUi("Order.ui", self)
        self.subtotalText.setText("0")
        self.loadKitchens()
        self.kitchensList.itemDoubleClicked.connect(self.loadMenu)
        self.returnBTN.clicked.connect(self.goBack)
        self.menuList.itemDoubleClicked.connect(self.addToOrder)

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
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Kitchens/" + nameOfKitchen

        # store the response of URL
        response = urlopen(url)

        # storing the JSON response
        # # from url in data
        data_json = json.loads(response.read())
        self.menuList.clear()
        myArray = data_json.keys()
        for val in myArray:
            if (data_json[val]["Available"]):
                self.menuList.addItem(str(val) + ": $" + str(data_json[val]["Price"]))

    def addToOrder(self):
        itemToAdd = self.menuList.currentItem().text()
        temp = itemToAdd.split(':')
        itemToAdd2 = temp[0]
        self.orderList.addItem(itemToAdd2)
        subtotal = float(self.subtotalText.toPlainText())
        temp2 = itemToAdd.split('$')
        subtotal2 = float(temp2[1])
        subtotal = subtotal + subtotal2
        self.subtotalText.setText(str(subtotal))
        tax = subtotal * .08
        self.taxText.setText(str(tax))
        subtotal = float(self.subtotalText.toPlainText())
        self.totalText.setText(str(tax + subtotal))

#--------------------Select Option Window--------------------
class kitchenMenu(QDialog):
    def __init__(self):
        super(kitchenMenu, self).__init__()
        loadUi("KitchenMenu.ui", self)
        self.AddItemBTN.clicked.connect(self.addItem)
        self.updatePriceBTN.clicked.connect(self.updatePrice)
        self.updateAvailabilityBTN.clicked.connect(self.updateAvailability)
        self.viewKitchensBTN.clicked.connect(self.viewKitchens)
        self.RemoveItemBTN.clicked.connect(self.removeItem)
        self.orderDetailsBTN.clicked.connect(self.viewOrders)

    def addItem(self):
        kScreen = kitchenAddItem()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def updatePrice(self):
        kScreen = kitchenUpdatePrice()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def updateAvailability(self):
        kScreen = kitchenUpdateAvailability()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def viewKitchens(self):
        kScreen = KitchensScreen()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def removeItem(self):
        kScreen = KitchenRemoveItem()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def viewOrders(self):
        kScreen = KitchenSeeOrders()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Kitchens See orders window--------------------
class KitchenSeeOrders(QDialog):
    def __init__(self):
        super(KitchenSeeOrders, self).__init__()
        loadUi("KitchenOrderDetails.ui", self)
        self.loadOrders()
        self.returnBTN.clicked.connect(self.goBack)
    
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def loadOrders(self):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders"

        # store the response of URL
        response = urlopen(url)

        # storing the JSON response
        # # from url in data
        data_json = json.loads(response.read())
        self.listWidget.addItems(data_json)
        print(data_json)

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

#--------------------Kitchens Remove Item Window--------------------
class KitchenRemoveItem(QDialog):
    def __init__(self):
        super(KitchenRemoveItem, self).__init__()
        loadUi("KitchenRemoveItem.ui", self)
        self.ReturnButton.clicked.connect(self.goBack)
        self.ConfirmButton.clicked.connect(self.RemoveItem)
        self.fillBTN.clicked.connect(self.fillItems)

        url = "http://127.0.0.1:8000/Kitchens"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.kitchenBox.addItems(data_json)


    def fillItems(self):
        nameOfKitchen = self.kitchenBox.currentText()
        url = "http://127.0.0.1:8000/Kitchens/" + nameOfKitchen
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.itemBox.clear()
        self.itemBox.addItems(list(data_json.keys()))


    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def RemoveItem(self):
        if(len(self.itemBox.currentText()) > 0):
            r = requests.delete("http://localhost:8000/RemoveItemFromMenu/" + self.kitchenBox.currentText() + "/" +self.itemBox.currentText())


#--------------------Kitchens Update Price Window--------------------
class kitchenUpdatePrice(QDialog):
    def __init__(self):
        super(kitchenUpdatePrice, self).__init__()
        loadUi("KitchenUpdatePrice.ui", self)
        self.returnBTN.clicked.connect(self.goBack)
        self.finishBTN.clicked.connect(self.finish)
        self.fillBTN.clicked.connect(self.fillItems)
        #self.fillPriceBTN.clicked.connect(self.fillPrice)
        #fill kitchen combo box
        url = "http://127.0.0.1:8000/Kitchens"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.kitchenBox.addItems(data_json)


    def fillItems(self):
        nameOfKitchen = self.kitchenBox.currentText()
        url = "http://127.0.0.1:8000/Kitchens/" + nameOfKitchen
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.itemBox.clear()
        self.itemBox.addItems(list(data_json.keys()))

    #TODO: FINISHE IMPLEMENTING THIS
    #def fillPRice(self):
        #textCost.setText()
    
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        
    def finish(self):
        if(len(self.itemBox.currentText()) > 0):
                    r = requests.put("http://localhost:8000/UpdateItemPrice/" + self.kitchenBox.currentText() + "/" + self.itemBox.currentText() + "?price=" + self.textCost.toPlainText())
                    self.textCost.setText("")
                    

#--------------------Kitchens Update Availability Window--------------------
class kitchenUpdateAvailability(QDialog):
    def __init__(self):
        super(kitchenUpdateAvailability, self).__init__()
        loadUi("KitchenUpdateAvailability.ui", self)
        self.returnBTN.clicked.connect(self.goBack)
        self.finishBTN.clicked.connect(self.finish)
        self.fillBTN.clicked.connect(self.fillItems)

        url = "http://127.0.0.1:8000/Kitchens"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.kitchenBox.addItems(data_json)


    def fillItems(self):
        nameOfKitchen = self.kitchenBox.currentText()
        url = "http://127.0.0.1:8000/Kitchens/" + nameOfKitchen
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.itemBox.clear()
        self.itemBox.addItems(list(data_json.keys()))

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)
        
    def finish(self):
        if(len(self.itemBox.currentText()) > 0):
            if(self.checkBox.checkState()): 
                available = True
            else: available = False
            r = requests.put("http://localhost:8000/UpdateItemAvailability/" + self.kitchenBox.currentText() + "/" + self.itemBox.currentText() + "?availability=" + str(available))
                

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