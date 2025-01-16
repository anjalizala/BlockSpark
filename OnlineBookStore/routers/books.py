from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas,  auth
from database import get_db
from models import Book

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)

@router.post("/books", tags=["Books"])
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),):
    # Check if the current user is an admin
    if current_user.role != "admin":  # Role extracted from the JWT token
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create books.",
        )
    
    # Admin is allowed to create books
    new_book = models.Book(**book.dict())
    
    if not new_book.title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")
    
    if not new_book.author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author Name is required")
    
    if not new_book.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price is required")
    
    if not new_book.quantity_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity is required")
    
    if new_book.title.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter valid Book Name")
    
    for char in new_book.author:
        if not (char.isalpha()):  
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter valid author name")
    # if new_book.author.isdigit():
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter valid author name")
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/GET")
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router.get("/GET/{bid}")
def get_book_id(bid : int,db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id==bid).first()
    return db_book

@router.post("/Delete/{id}")
def delete_book(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create books.",
        )
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book Not Found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted Successfully"}

# current_user= auth.get_current_user
# if current_user.role == "admin":
@router.post("/Update/{id}")
def update_book(id: int, title: str = None, author: str =None, price : int =None, qty: int = None, db: Session = Depends(get_db),
                current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create books.",
        )
    db_book = db.query(Book).filter(Book.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not Found")
    if title:
        db_book.title = title
    if author:
        db_book.author = author
    if price:
        db_book.price = price
    if qty:
        db_book.quantity_available = qty
    db.commit()
    db.refresh(db_book)
    return db_book
