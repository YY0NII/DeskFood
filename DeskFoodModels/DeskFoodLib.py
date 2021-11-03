from typing import List, Optional, Sequence, Type
from pydantic import BaseModel

# An item in the menu is a food item with a name, price, availability and description
class Item(BaseModel):
    name: str
    price: float
    available: bool
    description: Optional[str] = None

# A menu is a list of items
class Menu(BaseModel):
    items: List[Item]
    
class Kitchen(BaseModel):
    name: str
    location: str
    rating: int
    menu: Menu

# An OrderItem is composed of an item and the restuarant that the item is from
class OrderItem(BaseModel):
    from_kitchen: str
    item: Item

# An Order should have a unique ID, a user ID [Optional], a list of order items, and a total price
class Order(BaseModel):
    id: int
    user_id: Optional[int] = None
    items: List[OrderItem]
    total: float
    status: str