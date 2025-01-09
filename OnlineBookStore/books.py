from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from model import Book,User
from database import sessionLocal
from fastapi.security import OAuth2PasswordBearer
import users,auth

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/Add_book")
def create_book(title: str, author: str,price: float, qty: int):
    db = sessionLocal()
    db_book = Book(title=title,author=author, price=price, qty=qty)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
    
@router.get("/get_books")
def get_book():
    db = sessionLocal()
    db_book = db.query(Book).all()
    return db_book

@router.get("/get_books/{id}")
def get_book_id(id: int):
    db = sessionLocal()
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book Not Available")
    return db_book

@router.post("/update_books/{id}")
def update_book(id: int, title: str = None, author: str = None, price: float = None, qty: int = None):
    db = sessionLocal()
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not Found")
    if title:
        db_book.title = title
    if author:
        db_book.author = author
    if price:
        db_book.price = price
    if qty:
        db_book.qty = qty
    db.commit()
    db.refresh(db_book)
    return db_book


@router.post("/delete_books/{id}")
def delete_book(id: int):
    db = sessionLocal()
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book Not Found")
    db.delete(db_book)
    db.commit()
    return{"message":"Book deleted Successfully..."}