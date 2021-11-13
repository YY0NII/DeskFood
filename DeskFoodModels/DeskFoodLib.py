from typing import List, Optional, Sequence, Type
from pydantic import BaseModel
import enum

# Enum for order status
class OrderStatus(enum.Enum):
    pending = 'pending'
    cooking = 'cooking'
    ready = 'ready'
    onTheWay = 'on the way'
    delivered = 'delivered'

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

# An Order should have a user ID [Optional], a list of items, an order status, and a total price
class Order(BaseModel):
    order_id: Optional[str] = None
    user_id: str
    items: List[Item]
    total: float = 0.0
    status: OrderStatus = OrderStatus.pending
    kitchen: KitchenNames
    instructions: Optional[str] = None
    # Thinking of tying the order to a kitchen instead of having an order item
    # A user would have the choice to order from a kitchen and then pick something from the market
    # Or they could order from the market directly without needing a kitchen order
    # So on the database from_Kitchen would either be a kitchen or market. 
    # This is because a kitchen order can contain a market order but not the other way around
    # Should also contain the name of the person who ordered

    # Gonna have to add an Orders table to the Kitchens, Runners, and users tables