from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr
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
    

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserOut(BaseModel):
    username: str
    email : str
    id : int
    created_at : datetime

# class CartItem(BaseModel):
#     book_id: int
#     quantity: int

# class OrderCreate(BaseModel):
#     cart_items: List[CartItem]
#     total_price: float
