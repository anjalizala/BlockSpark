from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(30), unique=True, index=True)
    type = Column(String(30), default=0)  # "admin" or "customer"
    password = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    author = Column(String(30))
    price = Column(Float)
    quantity_available = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    
class Cart(Base):
    __tablename__ = "carts"
    id =Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete= "CASCADE"))
    quantity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(30), default="pending")
    created_at = Column(DateTime, default=datetime.now)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

