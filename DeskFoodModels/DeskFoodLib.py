from typing import List, Sequence, Type
from pydantic import BaseModel

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