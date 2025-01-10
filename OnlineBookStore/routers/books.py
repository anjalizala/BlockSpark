from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database, auth
from database import get_db

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
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/GET")
def get_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()
