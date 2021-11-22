from fastapi.testclient import TestClient
import sys
sys.path.append('../')
from Backend.DeskFoodAPI import app


client = TestClient(app)

# TODO: Add more tests

def test_read_Kitchens():
    response = client.get("/Kitchens")
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}

def test_read_Orders():
    response = client.get("/Orders")
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}