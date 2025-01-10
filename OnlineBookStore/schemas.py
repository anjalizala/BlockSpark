from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    quantity_available: int
    
class UserOut(BaseModel):
    username: str
    email : str
    id : int
    created_at : datetime

class CartItem(BaseModel):
    book_id: int
    quantity: int

# class OrderCreate(BaseModel):
#     cart_items: List[CartItem]
#     total_price: float
