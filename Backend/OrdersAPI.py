import pyrebase
from fastapi import FastAPI
import sys
sys.path.append('../')

from DeskFoodModels.DeskFoodLib import Order, OrderItem
from typing import List

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

# -----------------------CREATE-----------------------
# CREATES NEW ORDER
@app.post("/CreateNewOrder")
def createOrder(order: Order):
    # Sets the Order
    db.child("Orders").push(order)

    return {}

# -----------------------READ-----------------------

# -----------------------UPDATE-----------------------

# -----------------------DELETE-----------------------
