from typing import List, Optional, Sequence, Type
from pydantic import BaseModel
import enum

# Enum for order status
class OrderStatus(enum.Enum):
    PENDING = 'Pending'
    COOKING = 'Cooking'
    PREPARING = 'Preparing'
    READY = 'Ready'
    ON_THE_WAY = 'On the way'
    DELIVERED = 'Delivered'

# Enum for Kitchen names
class KitchenNames(enum.Enum):
    freshens = 'Freshens'
    burgers = 'Burgers'
    pizza = 'Pizza'
    deli = 'Deli'
    market = 'Market'
    
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
    name: KitchenNames
    location: str
    rating: int
    menu: Menu

# An Order should have a user ID, a list of items, an order status, and a total price
class Order(BaseModel):
    order_id: Optional[str] = None
    user_id: str
    runner_id:Optional[str] = None
    delivery_location: str
    items: List[str] 
    total: float = 0.0
    status: OrderStatus = OrderStatus.PENDING
    instructions: Optional[str] = None