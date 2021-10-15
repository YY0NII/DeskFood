import pyrebase
from fastapi import FastAPI

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

# data = {
#     'menu': { 
#         'Rice Bowls': {'Mexican Rice Bowl': { 'price': 10.30, 'status': available } , 'Asian Rice Bowl': 10.30},
#         'Flatbreads': {'Chipotle Chicken Club': 7.10 , 'Chicken Club': 7.10},
#         'Salads': {'Chicken Salad': 5.25 , 'Greek Salad': 5.25} 
#     },
#     'location': 'Somewhere',
#     'rating': 5
# }

# db.child("Kitchen").child("Freshens").set(data)

# -----------------------CREATE-----------------------
# CREATE A NEW KITCHEN
# CREATE A NEW ITEM FOR A KITCHENS MENU

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
# UPDATE A KITCHEN'S MENU ITEM
# UPDATE A KITCHEN'S LOCATION
# UPDATE A KITCHEN'S RATING

# -----------------------DELETE-----------------------
# DELETE A KITCHEN
# DELETE A KITCHEN'S MENU ITEM