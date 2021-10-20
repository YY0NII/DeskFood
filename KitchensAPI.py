from typing import List, Sequence, Type
import pyrebase
from fastapi import FastAPI
from pydantic import BaseModel

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

class Item(BaseModel):
    name: str
    price: float
    status: str

class Menu(BaseModel):
    items: List[Item]
class Kitchen(BaseModel):
    name: str
    location: str
    rating: int
    menu: Menu



# db.child("Kitchen").child("Freshens").set(data)
#Method to convert a list of items is into a dictionary
def listToDict(items):
    values = {}
    for i in items:
        values.update({i.name:{"Price":i.price, "Status": i.status}})
        print(i)
    
    return values


# -----------------------CREATE-----------------------
# CREATE A NEW KITCHEN
@app.post("/CreateKitchen")
def createKitchen(kitchen: Kitchen):
    # Sets the Menu
    db.child("Kitchen").child(kitchen.name).child("Menu").set(listToDict(kitchen.menu.items))

    # Sets the Location
    db.child("Kitchen").child(kitchen.name).child("Location").set(kitchen.location)

    # Sets the Rating
    db.child("Kitchen").child(kitchen.name).child("Rating").set(kitchen.rating)

    return {}

# CREATES NEW MENU FOR A KITCHEN
@app.post("/CreateNewMenu/{kitchenName}")
def createMenu(items: List[Item], kitchenName):
    #Overrides the menu of kitchen currently on the Database
    db.child("Kitchen").child(kitchenName).child("Menu").set(listToDict(items))
    
    return {}

# -----------------------READ-----------------------
# READ ALL KITCHENS
@app.get("/Kitchens")
def getKitchens():
    kitchens = db.child("Kitchen").get()
    return kitchens.val()

# READ ALL ITEMS FOR A KITCHEN
@app.get("/Kitchens/{kitchenName}")
def getKitchenMenu(kitchenName):
    kitchen = db.child("Kitchen").child(kitchenName).child("menu").get()
    return kitchen.val()

# -----------------------UPDATE-----------------------
# UPDATES MENU WITH NEW ITEM(S) 
@app.put("/AddToMenu/{kitchenName}")
def addToMenu(items: List[Item], kitchenName):
    db.child("Kitchen").child(kitchenName).child("Menu").update(listToDict(items))
    
    return {}

# UPDATE A KITCHEN'S MENU ITEM PRICE
@app.put("/UpdateItemPrice/{kitchenName}/{itemName}")
def updateItemPrice(kitchenName, itemName, price: float):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Price").set(price)
    return {}

# UPDATE A KITCHEN'S MENU ITEM STATUS
@app.put("/UpdateItemStatus/{kitchenName}/{itemName}")
def updateItemStatus(kitchenName, itemName, status: str):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).child("Status").set(status)
    return {}

# UPDATE A KITCHEN'S LOCATION
@app.put("/UpdateKitchenLocation/{kitchenName}")
def updateKitchenLocation(kitchenName, location: str):
    db.child("Kitchen").child(kitchenName).child("Location").set(location)
    return {}

# UPDATE A KITCHEN'S RATING
@app.put("/UpdateKitchenRating/{kitchenName}")
def updateKitchenRating(kitchenName, rating: int):
    db.child("Kitchen").child(kitchenName).child("Location").set(rating)
    return {}

# -----------------------DELETE-----------------------
# DELETE A KITCHEN
@app.delete("/RemoveKitchen/{kitchenName}")
def deleteKitchen(kitchenName):
    # Sets the Menu
    db.child("Kitchen").child(kitchenName).remove()

    return {}

# DELETE A KITCHEN'S MENU ITEM
@app.delete("/RemoveItemFromMenu/{kitchenName}/{itemName}")
def deleteItem(kitchenName, itemName):
    db.child("Kitchen").child(kitchenName).child("Menu").child(itemName).remove()
    return {}