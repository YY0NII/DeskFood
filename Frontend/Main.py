from os import name
import sys
import requests
import time
import threading
sys.path.append('../')
from DeskFoodModels.DeskFoodLib import Item, OrderStatus, Order
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QApplication, QListWidget, QMenu, QPushButton, QStackedWidget, QTextBrowser, QWidget
from urllib.request import urlopen
import json
from DeskFoodModels import firebaseAuth

#---Global Variables---#
#orderID = ""
#order = Order()
userID = ""

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
        global userID
        userID =self.user["localId"]

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
                    global userID
                    userID = self.user["localId"]
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
        kScreen = RunnerPickOrder()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Runner Pick Orders Window--------------------
class RunnerPickOrder(QDialog):
    def __init__(self):
        super(RunnerPickOrder, self).__init__()
        loadUi("RunnerPickOrder.ui", self)
        self.loadOrders()
        self.returnBTN.clicked.connect(self.goBack)
        self.orderList.itemDoubleClicked.connect(self.orderDetails)
    
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def loadOrders(self):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders/Status/Ready"

        # store the response of URL
        response = urlopen(url)

        # storing the JSON response
        # # from url in data
        data_json = json.loads(response.read())

        # Clear orderList
        self.orderList.clear()
        # iterate over the data and append the id of the orders to a list
        for i in range(len(data_json)):
            self.orderList.addItem(data_json[i]['order_id'])

    def orderDetails(self):
        # Switch to the order details window
        kScreen = RunnerOrderDetails(orderID=self.orderList.currentItem().text())
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Runner Order Details Window--------------------
class RunnerOrderDetails(QDialog):
    def __init__(self, orderID):
        super(RunnerOrderDetails, self).__init__()
        loadUi("RunnerOrderDetails.ui", self)
        self.returnBTN.clicked.connect(self.goBack)
        self.setCustomer(orderID)
        self.setOrder(orderID)
        self.setOrderItems(orderID)
        self.setDeliveryLocation(orderID)
        self.setOrderStatus(orderID)
        self.setOrderTotal(orderID)
        self.setOrderInstructions(orderID)
        self.statusButton.clicked.connect(self.changeStatusToEnRoute)

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    # Set the customer label to the userID of the order
    def setCustomer(self, orderID):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/UserID"
        response = urlopen(url)
        userID = json.loads(response.read())

        self.customerIDLabel.setText(userID)

    # Set the order label to the orderID of the order
    def setOrder(self, orderID):
        self.orderIDLabel.setText(orderID)

    # Populate the items list with the items in the order
    def setOrderItems(self, orderID):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Items"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.itemsList.addItems(data_json)

    # Set the delivery location label to the delivery location of the order
    def setDeliveryLocation(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/DeliveryLocation"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.deliveryLocationLabel.setText(data_json)

    # Set the order status label to the order status of the order
    def setOrderStatus(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Status"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.orderStatusLabel.setText(data_json)

    # Set the order total label to the order total of the order
    def setOrderTotal(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Total"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.orderTotalLabel.setText("$" + str(data_json))

    # Set the order instructions label to the order instructions of the order
    def setOrderInstructions(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Instructions"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.orderInstructionsLabel.setText(data_json)

    def changeStatusToEnRoute(self):
        orderID = self.orderIDLabel.text()
        #Update the order status to en route
        r = requests.put("http://localhost:8000/Orders/" + orderID + "/Status" + "?status=" + OrderStatus.ON_THE_WAY.value)
        #Update the order RunnerID to the current runner
        r = requests.put("http://localhost:8000/Orders/" + orderID + "/RunnerID" + "?runnerId=" + userID)
        self.setOrderStatus(orderID)
        self.statusButton.setText("Confirm Delivery")
        self.statusButton.clicked.connect(self.changeStatusToDelivered)
    
    def changeStatusToDelivered(self):
        orderID = self.orderIDLabel.text()
        #Update the order status to delivered
        r = requests.put("http://localhost:8000/Orders/" + orderID + "/Status" + "?status=" + OrderStatus.DELIVERED.value)
        self.setOrderStatus(orderID)
        #Switch back to the RunnerPickOrder window
        widget.setCurrentIndex(widget.currentIndex() - 1) 
        widget.currentWidget().loadOrders()
        widget.removeWidget(self)

#--------------------Order Window----------------------------
class orderWindow(QDialog):
    def __init__(self):
        super(orderWindow, self).__init__()
        loadUi("Order.ui", self)
        self.subtotalText.setText("0")
        self.loadKitchens()
        self.kitchensList.itemDoubleClicked.connect(self.loadMenu)
        self.returnBTN.clicked.connect(self.goBack)
        self.menuList.itemDoubleClicked.connect(self.addToOrder)
        self.finishBTN.clicked.connect(self.finish)

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
                self.menuList.addItem(str(val) + ": $" + "%0.2f" % float(data_json[val]["Price"]))

    def addToOrder(self):
        itemToAdd = self.menuList.currentItem().text()
        temp = itemToAdd.split(':')
        itemToAdd2 = temp[0]
        self.orderList.addItem(itemToAdd2)
        subtotal = float(self.subtotalText.toPlainText())
        temp2 = itemToAdd.split('$')
        subtotal2 = float(temp2[1])
        subtotal = round(subtotal + subtotal2, 2)
        self.subtotalText.setText( "%0.2f" % subtotal )
        tax = round(subtotal * .08, 2) 
        self.taxText.setText( "%0.2f" % tax)
        subtotal = float(self.subtotalText.toPlainText())
        self.totalText.setText( "%0.2f" % round(tax + subtotal, 2) )


    def finish(self):
        kScreen = OrderConfirmaiton(self.orderList, self.totalText.toPlainText())
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Order Confirmation Window----------------------------
class OrderConfirmaiton(QDialog):
    def __init__(self, orderList, total):
        super(OrderConfirmaiton, self).__init__()
        loadUi("OrderConfirmation.ui", self)
        self.returnBTN.clicked.connect(self.goBack)
        self.ConfirmBTN.clicked.connect(self.finish)
        for i in range(orderList.count()):
            self.orderItemList.addItem(orderList.item(i).text())

        self.TotalField.setText(total)
        self.DeliveryLocation.returnPressed.connect(self.enableConfirmButton)
        # The Button should not be enabled until the user has entered their location   
        self.ConfirmBTN.setEnabled(False)

    #Method to enable the confirm button
    def enableConfirmButton(self):
        # Check if the location is empty
        if self.DeliveryLocation.text() != "":
            self.ConfirmBTN.setEnabled(True)

    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def finish(self):
        orderItems = []
        for i in range(self.orderItemList.count()):
            orderItems.append(self.orderItemList.item(i).text())

        order = Order(
            user_id = userID,
            delivery_location = self.DeliveryLocation.text(),
            items = orderItems,  
            total = self.TotalField.text(), 
            instructions = self.Instructions.text()
        )
        
        kScreen = paymentWindow(order)
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Payment Window--------------------
class paymentWindow(QDialog):
    def __init__(self, order):
        super(paymentWindow, self).__init__()
        loadUi("Payment.ui", self)
        self.setWindowTitle("Payment")
        self.returnBTN.clicked.connect(self.goBack)
        self.studentIDCheck.clicked.connect(self.clickSID)
        self.debitcreditCheck.clicked.connect(self.clickDCC)
        # Don't know why this works but stack overflow says it does
        self.finishBTN.clicked.connect(lambda: self.finish(order))      
        
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def clickSID(self):
        self.studentIDCheck.setChecked(1)
        self.debitcreditCheck.setChecked(0)
        self.fullName.setHidden(True)
        self.ccNumber.setHidden(True)
        self.expDate.setHidden(True)
        self.CVV.setHidden(True)
        self.nameInput.setHidden(True)
        self.dccInput.setHidden(True)
        self.expInput.setHidden(True)
        self.cvvInput.setHidden(True)
        self.studentID.setHidden(False)
        self.idInput.setHidden(False)

    def clickDCC(self):
        self.studentIDCheck.setChecked(0)
        self.debitcreditCheck.setChecked(1)
        self.studentID.setHidden(True)
        self.idInput.setHidden(True)
        self.fullName.setHidden(False)
        self.ccNumber.setHidden(False)
        self.expDate.setHidden(False)
        self.CVV.setHidden(False)
        self.nameInput.setHidden(False)
        self.dccInput.setHidden(False)
        self.expInput.setHidden(False)
        self.cvvInput.setHidden(False)

    def finish(self, order):
        #Stores the orderID that's created in the database
        r = requests.post("http://127.0.0.1:8000/CreateNewOrder", order.json())
        #print(r.text)
        kScreen = statusWindow(r.text)
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Order Status Window--------------------
class statusWindow(QDialog):
    def __init__(self, orderID):
        self.x = 1
        super(statusWindow, self).__init__()
        loadUi("OrderStatus.ui", self)
        self.setWindowTitle("Order Status")
        self.orderStatusBTN.clicked.connect(lambda: self.orderStatus(orderID))
        #BUG: This solution doesn't work well with the way that I'm passing the orderID
        #threading.Thread(target=self.update(orderID), daemon=True).start()
        #self.homeBTN.clicked.connect(self.home)

    # def closeEvent(self, event):
    #     self.x = 0
        
    # def update(self, orderID):
    #     print("hello")
    #     self.orderStatus(orderID)
    #     time.sleep(1)
    #     if(self.x == 1):
    #         self.update(orderID)

    def orderStatus(self, orderID):
        # print("This is what we're getting" + orderID)
        #NOTE: This is a bit of a hack, idk why the orderID keeps the " " around it
        url = "http://127.0.0.1:8000/Orders/" + orderID.replace('"', "") + "/Status"
        #url = "http://127.0.0.1:8000/Orders/" + "-Mpr0leituNsBbqY2CDq" + "/Status"
        response = urlopen(url)
        data_json = json.loads(response.read())

        if (data_json == OrderStatus.PENDING.value):
            self.statusLBL.setText("Order is pending!")
        elif (data_json == OrderStatus.PREPARING.value):
            self.statusLBL.setText("Preparing the order!")
        elif (data_json == OrderStatus.COOKING.value):
            self.statusLBL.setText("Cooking Order!")
        elif (data_json == OrderStatus.READY.value):
            self.statusLBL.setText("Order is ready!")
        elif (data_json == OrderStatus.ON_THE_WAY.value):
            self.statusLBL.setText("Order is on the way!")
        elif (data_json == OrderStatus.DELIVERED.value):
            self.statusLBL.setText("Order is delivered!")
        else:
            self.statusLBL.setText("Something went wrong!")
    
    """def home(self):
        kScreen = orderWindow()
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)"""

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
        self.orderList.itemDoubleClicked.connect(self.orderDetails)
    
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.removeWidget(self)

    def loadOrders(self):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders/Status/Pending"

        # store the response of URL
        response = urlopen(url)

        # storing the JSON response
        # # from url in data
        data_json = json.loads(response.read())

        # Clear orderList
        self.orderList.clear()
        # iterate over the data and append the id of the orders to a list
        for i in range(len(data_json)):
            self.orderList.addItem(data_json[i]['order_id'])

    def orderDetails(self):
        # Switch to the order details window
        kScreen = KitchenSeeOrdersDetails(orderID=self.orderList.currentItem().text())
        widget.addWidget(kScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

#--------------------Expanded Kitchens order details window--------------------
class KitchenSeeOrdersDetails(QDialog):
    def __init__(self, orderID):
        super(KitchenSeeOrdersDetails, self).__init__()
        loadUi("OrderDetail.ui", self)
        self.setCustomer(orderID)
        self.setOrder(orderID)
        self.setOrderItems(orderID)
        self.setDeliveryLocation(orderID)
        self.setOrderStatus(orderID)
        self.setOrderTotal(orderID)
        self.setOrderInstructions(orderID)
        self.statusButton.clicked.connect(self.changeStatusToCooking)

    # Set the customer label to the userID of the order
    def setCustomer(self, orderID):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/UserID"
        response = urlopen(url)
        userID = json.loads(response.read())

        self.customerIDLabel.setText(userID)

    # Set the order label to the orderID of the order
    def setOrder(self, orderID):
        self.orderIDLabel.setText(orderID)

    # Populate the items list with the items in the order
    def setOrderItems(self, orderID):
        # parameter for urlopen
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Items"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.itemsList.addItems(data_json)

    # Set the delivery location label to the delivery location of the order
    def setDeliveryLocation(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/DeliveryLocation"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.deliveryLocationLabel.setText(data_json)

    # Set the order status label to the order status of the order
    def setOrderStatus(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Status"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.orderStatusLabel.setText(data_json)

    # Set the order total label to the order total of the order
    def setOrderTotal(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Total"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.orderTotalLabel.setText(str(data_json))

    # Set the order instructions label to the order instructions of the order
    def setOrderInstructions(self, orderID):
        url = "http://127.0.0.1:8000/Orders" + "/" + orderID + "/Instructions"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.orderInstructionsLabel.setText(data_json)

    def changeStatusToCooking(self):
        orderID = self.orderIDLabel.text()
        #Update the order status to cooking
        r = requests.put("http://localhost:8000/Orders/" + orderID + "/Status" + "?status=" + OrderStatus.COOKING.value)
        self.setOrderStatus(orderID)
        self.statusButton.setText("Complete Order")
        self.statusButton.clicked.connect(self.completeOrder)

    def completeOrder(self):
        orderID = self.orderIDLabel.text()
        #Update the order status to complete
        r = requests.put("http://localhost:8000/Orders/" + orderID + "/Status" + "?status=" + OrderStatus.READY.value)
        self.setOrderStatus(orderID)
        #Switch back to the kitchenorders window
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.currentWidget().loadOrders()
        widget.removeWidget(self)



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
        self.fillPriceBTN.clicked.connect(self.fillPrice)
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

    def fillPrice(self):
        nameOfKitchen = self.kitchenBox.currentText()
        nameOfItem = self.itemBox.currentText()
        #NOTE: this is a bit of a hack, but it works. Essentially the URL does not like spaces in the item name, so I had to replace them with '%20'.
        url = "http://127.0.0.1:8000/Kitchens/" + nameOfKitchen + "/" + nameOfItem.replace(' ', '%20') + "/Price"
        response = urlopen(url)
        data_json = json.loads(response.read())
        self.textCost.setText(str(data_json))
    
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