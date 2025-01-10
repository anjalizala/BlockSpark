from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Cart,User,Book
from schemas import CartItem
import auth

router = APIRouter(  prefix="/carts",tags=["Cart"],)

@router.post("/Add")
def add_to_cart(id: int, quantity: int, db: Session = Depends(get_db), current_user : User = Depends(auth.get_current_user)):
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can add to cart.",
        )
    db_cart = db.query(Book).filter(Book.id == id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Book not found")
    
    cart_item = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.book_id == id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id = current_user.id, book_id = id, quantity = quantity)
        db.add(cart_item)
    db.commit()
    return {"message": "Book added to cart"}

@router.get("/View")
def view_cart(db: Session = Depends(get_db), current_user : User = Depends(auth.get_current_user)):
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can access.",
        )
    db_cart = db.query(Cart).filter(User.id == current_user.id).all()
    #book = db.query(Book).filter(Book.id == db_cart.)
    response = []
    for item in db_cart:
        # Fetch the book details for each cart item
        book = db.query(Book).filter(Book.id == item.book_id).first()
        if book:  # Ensure the book exists
            response.append({
                "book_id": item.book_id,
                "book_title": book.title,
                "quantity": item.quantity,
                "added_at": item.created_at,
            })
    return response

@router.post("/Update")
def update_cart(book_id: int, quantity: int ,db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users access.",
        )
    db_cart = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.book_id == book_id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Item not in the Cart")
    
    if quantity <= 0:
        db.delete(db_cart)
    else:
        db_cart.quantity = quantity
        
    db.commit()
    db.refresh(db_cart)
    return db_cart
        
@router.post("/Delete/{id}")
def delete_cart(id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can access",
        )
    db_cart = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.book_id ==id).first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Item not in the cart")
    
    db.delete(db_cart)
    db.commit()
    return {"message": "Item removed"}