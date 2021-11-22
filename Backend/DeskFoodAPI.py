import pyrebase
from fastapi import FastAPI
import sys
sys.path.append('../')

from DeskFoodModels.DeskFoodLib import Kitchen, Menu, Item, Order
from typing import List, Sequence, Type

# Firebase Config - Required info to connect to Firebase
firebaseConfig = {
    'apiKey': "AIzaSyDU0ygdrujK-vkCQb7fRtkv2hGVbxV6A6I",
    'authDomain': "deskfoodapp.firebaseapp.com",
    'databaseURL': "https://deskfoodapp-default-rtdb.firebaseio.com",
    'projectId': "deskfoodapp",
    'storageBucket': "deskfoodapp.appspot.com",
    'messagingSenderId': "42027451518",
    'appId': "1:42027451518:web:69bb99b1689fafe5b2042f",
    'measurementId': "G-9M9EJD2HSH"
}

# Initializes connection to Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Initializes connection to Firebase Real Time Database
db = firebase.database()

# Initializes FastAPI module
app = FastAPI()

# ---------------------------------------------- Kitchens ----------------------------------------------

# ----------------------- HELPER METHODS -----------------------

# METHOD TO CONVERT A LIST OF ITEMS INTO A DICTIONARY
def listToDict(items):
    values = {}
    for i in items:
        values.update({i.name:{"Price":i.price, "Available": i.available, "Description": i.description}})
        print(i)
    
    return values

# ----------------------- CREATE -----------------------

# CREATE A NEW KITCHEN
@app.post("/CreateKitchen", tags=["Kitchen"])
def createKitchen(kitchen: Kitchen):
    # Sets the Menu
    db.child("Kitchen").child(kitchen.name.value).child("Menu").set(listToDict(kitchen.menu.items))

    # Sets the Location
    db.child("Kitchen").child(kitchen.name.value).child("Location").set(kitchen.location)

    # Sets the Rating
    db.child("Kitchen").child(kitchen.name.value).child("Rating").set(kitchen.rating)

    return {}

# CREATES NEW MENU FOR A KITCHEN
@app.post("/CreateNewMenu/{kitchenName}", tags=["Kitchen"])
def createMenu(items: List[Item], kitchenName):
    #Overrides the menu of kitchen currently on the Database
    db.child("Kitchen").child(kitchenName).child("Menu").set(listToDict(items))
    
    return {}

# ----------------------- READ -----------------------

# READ ALL KITCHENS
@app.get("/Kitchens", tags=["Kitchen"])
def getKitchens():
    kitchens = db.child("Kitchen").get()
    return kitchens.val()

# READ ALL ITEMS FOR A KITCHEN
@app.get("/Kitchens/{kitchenName}", tags=["Kitchen"])
def getKitchenMenu(kitchenName):
    kitchen = db.child("Kitchen").child(kitchenName).child("Menu").get()
    return kitchen.val()

# READ THE PRICE OF AN ITEM
@app.get("/Kitchens/{kitchenName}/{itemName}/Price", tags=["Kitchen"])
def getItemPrice(kitchenName, itemName):
    item = db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Price").get()
    return item.val()

# READ THE AVAILABILITY OF AN ITEM
@app.get("/Kitchens/{kitchenName}/{itemName}/Availability", tags=["Kitchen"])
def getItemAvailability(kitchenName, itemName):
    item = db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Available").get()
    return item.val()

# ----------------------- UPDATE -----------------------

# UPDATES MENU WITH NEW ITEM(S) 
@app.put("/AddToMenu/{kitchenName}", tags=["Kitchen"])
def addToMenu(item: Item, kitchenName):
    db.child("Kitchen").child(kitchenName).child("Menu").child(item.name).child("Price").set(item.price)
    db.child("Kitchen").child(kitchenName).child("Menu").child(item.name).child("Available").set(item.available)
    db.child("Kitchen").child(kitchenName).child("Menu").child(item.name).child("Description").set(item.description)
    
    return {}

# UPDATE A KITCHEN'S MENU ITEM PRICE
@app.put("/UpdateItemPrice/{kitchenName}/{itemName}", tags=["Kitchen"])
def updateItemPrice(kitchenName, itemName, price: float):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Price").set(price)
    return {}

# UPDATE A KITCHEN'S MENU ITEM AVAILABILITY
@app.put("/UpdateItemAvailability/{kitchenName}/{itemName}", tags=["Kitchen"])
def updateItemAvailability(kitchenName, itemName, availability: bool):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Available").set(availability)
    return {}

# UPDATE A KITCHEN'S MENU ITEM DESCRIPTION
@app.put("/UpdateItemDescription/{kitchenName}/{itemName}", tags=["Kitchen"])
def updateItemDescription(kitchenName, itemName, description: str):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Description").set(description)
    return {}

# UPDATE A KITCHEN'S LOCATION
@app.put("/UpdateKitchenLocation/{kitchenName}", tags=["Kitchen"])
def updateKitchenLocation(kitchenName, location: str):
    db.child("Kitchen").child(kitchenName).child("Location").set(location)
    return {}

# UPDATE A KITCHEN'S RATING
@app.put("/UpdateKitchenRating/{kitchenName}", tags=["Kitchen"])
def updateKitchenRating(kitchenName, rating: int):
    db.child("Kitchen").child(kitchenName).child("Location").set(rating)
    return {}

# ----------------------- DELETE -----------------------

# DELETE A KITCHEN
@app.delete("/RemoveKitchen/{kitchenName}", tags=["Kitchen"])
def deleteKitchen(kitchenName):
    # Sets the Menu
    db.child("Kitchen").child(kitchenName).remove()

    return {}

# DELETE A KITCHEN'S MENU ITEM
@app.delete("/RemoveItemFromMenu/{kitchenName}/{itemName}", tags=["Kitchen"])
def deleteItem(kitchenName, itemName):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).remove()
    return {}


# ---------------------------------------------- Orders ----------------------------------------------

# ----------------------- Helper Methods -----------------------

# METHOD TO CONVERT A LIST OF ITEMS FROM AN ORDER INTO A DICTIONARY
def listToDictForOrders(items):
    values = {}
    values2 = {}
    for i in items:
        values.update({
            i.name:{
                "Price":i.price, 
                "Available": i.available, 
                "Description": i.description
            }
        })

        print(i)
    
    values2.update({"Items":values})

    return values2

# METHOD TO CONVERT A DICTIONARY INTO A LIST OF ITEMS FROM AN ORDER
def dictToListForOrders(items):
    values = []
    for i in items:
        values.append(Item(name = i, price = items[i]["Price"], available = items[i]["Available"], description = items[i]["Description"]))

    return values

# METHOD TO CONVERT A DICTIONARY INTO A LIST OF ORDERS FROM THE DATABASE
def dictToListForOrdersFromDatabase(orders):
    values = []
    for i in orders:
        values.append(
            Order(
                order_id = i, 
                user_id = orders[i]["UserID"], 
                items = dictToListForOrders(orders[i]["Items"]),  
                total = orders[i]["Total"], 
                status = orders[i]["Status"],
                kitchen = orders[i]["Kitchen"], 
                instructions = orders[i]["Instructions"]
            )
        )

    return values

# METHOD TO RETURN A LIST OF ORDERS WITH A SPECIFIC KITCHEN NAME
def getOrdersWithKitchenName(orders, kitchenName):
    values = []
    for i in orders:
        if i.kitchen.value == kitchenName:
            values.append(i)

    return values

# METHOD TO RETURN A LIST OF ORDERS WITH A SPECIFIC STATUS
def getOrdersWithStatus(orders, status):
    values = []
    for i in orders:
        if i.status == status:
            values.append(i)

    return values

# METHOD TO RETURN A LIST OF ORDERS WITH A SPECIFIC USER ID
def getOrdersWithUserID(orders, userID):
    values = []
    for i in orders:
        if i.user_id == userID:
            values.append(i)

    return values

# ----------------------- CREATE -----------------------

# CREATES NEW ORDER
@app.post("/CreateNewOrder", tags=["Order"])
def createOrder(order: Order):
    # Sets the Order Saves dictionary with the key that is generated by Firebase
    theOrder = db.child("Orders").push(listToDictForOrders(order.items))

    # Saves the actual key of the Order
    orderId = theOrder.get("name")

    # Sets the attributes of the Order
    db.child("Orders").child(orderId).child("Total").set(order.total)
    db.child("Orders").child(orderId).child("Status").set(order.status.value)

    # TODO: Should verify that the userid exists before setting it
    db.child("Orders").child(orderId).child("UserID").set(order.user_id)

    db.child("Orders").child(orderId).child("Kitchen").set(order.kitchen.value)
    db.child("Orders").child(orderId).child("Instructions").set(order.instructions)

    # # Send the Order ID to the appropriate Kitchen
    # db.child("Kitchen").child(order.kitchen.value).child("Orders").child(orderId).set(order.user_id)
    
    # # Send the Order ID to the User
    # db.child("Users").child(order.user_id).child("Orders").child(orderId).set(order.user_id)

    return orderId

# ----------------------- READ -----------------------
# READS ALL ORDERS
@app.get("/Orders", tags=["Order"])
def getAllOrders():
    # Gets all the Orders
    allOrders = db.child("Orders").get()
    print(allOrders.val())

    return allOrders.val()

# READS ORDER BY ID
@app.get("/Orders/{orderId}", tags=["Order"])
def getOrderById(orderId):
    # Gets the Order by the ID
    order = db.child("Orders").child(orderId).get()

    return order.val()

# READS ORDER STATUS BY ID
@app.get("/Orders/{orderId}/Status", tags=["Order"])
def getOrderStatusById(orderId):
    # Gets the Order by the ID
    order = db.child("Orders").child(orderId).child("Status").get()

    return order.val()

# READS ALL ORDERS BY USER ID
@app.get("/Orders/User/{userId}", tags=["Order"])
def getAllOrdersByUserId(userId):
    # Gets all the Orders 
    allOrders = db.child("Orders").get()

    # Gets all the Orders with the User ID
    orders = getOrdersWithUserID(dictToListForOrdersFromDatabase(allOrders.val()), userId)

    #print(type(orders[0]))

    return orders

# READS ALL ORDERS BY KITCHEN NAME
@app.get("/Orders/Kitchen/{kitchenName}", tags=["Order"])
def getAllOrdersByKitchenName(kitchenName):
    # Gets all the Orders
    allOrders = db.child("Orders").get()

    # Gets all the Orders with the Kitchen Name
    orders = getOrdersWithKitchenName(dictToListForOrdersFromDatabase(allOrders.val()), kitchenName)

    return orders

# ----------------------- UPDATE -----------------------

# ----------------------- DELETE -----------------------
# DELETE A ORDER
@app.delete("/RemoveOrder/{orderId}", tags=["Order"])
def deleteOrder(orderId):
    # Sets the Order
    db.child("Orders").child(orderId).remove()

    return {}