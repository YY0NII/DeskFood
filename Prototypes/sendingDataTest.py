# This module is used to send data to the api
import requests

# This module and the following line are so that we can access the classes shored in the DeskFoodModels folder
import sys
sys.path.append('../')

# Import the class library that I made for this project
from DeskFoodModels.DeskFoodLib import Kitchen, Menu, Item

# The First step is to create an object from the models we have (Has to be in this exact format because I used Pydantic to make the models)
item = Item(name = "OneLastTest", price = 10, status = "Unavailable")

# We send the object to the api by using a put or post request (Depends on the end point your trying to hit, look at the api to see what you need)
# Thanks to the objects being made with pydantic we can convert them into json form by calling .json() on them
r = requests.put("http://localhost:8000/AddToMenu/Freshens", item.json()) 
