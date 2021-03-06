import pyrebase
import sys
sys.path.append('../')

from DeskFoodModels.DeskFoodLib import Kitchen, Menu, Item, OrderStatus, Order, OrderItem
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

boolTest = True

#print(db.push(boolTest))

#print(db.child("-MnWj3lGxUT7yweMlgfW").get().val())

#print(OrderStatus.pending.name)

#print(db.push(OrderStatus.pending.name))

order = Order(
    items = [
        OrderItem(
            from_kitchen = "Kitchen",
            item = Item(
                name = "",
                price = 0.0,
                available = True,
                description = ""
            )
        )
    ],
    total = 0.0
)

#print(order)
print(order.status.name)