from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    email = Column(String(30))
    password = Column(String(100))
    last_login = Column(DateTime, default=None)
    is_admin = Column(Boolean,default=False)
    
class Book(Base):
    __tablename__="books"
    id = Column(Integer,primary_key=True)
    title = Column(String(30), nullable=True)
    author = Column(String(30), nullable=True)
    price =  Column(Float, nullable=True)
    qty = Column(Integer,nullable=True)
    created_at = Column(DateTime, default=func.now())