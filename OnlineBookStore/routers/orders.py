from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Cart,User,Book, Order, OrderItem
import auth

router = APIRouter(  prefix="/orders",tags=["Orders"],)

@router.post("/place")
def place_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    # Fetch cart items
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Calculate total price and create order
    total_price = 0
    for item in cart_items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        if not book or book.quantity_available < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for Book ID {item.book_id}")
        total_price += book.price * item.quantity

    order = Order(user_id=current_user.id, total_price=total_price, status="pending")
    db.add(order)
    db.commit()
    db.refresh(order)

    # Create order items and update book inventory
    for item in cart_items:
        book = db.query(Book).filter(Book.id == item.book_id).first()
        book.quantity_available -= item.quantity
        order_item = OrderItem(
            order_id=order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            price=book.price,
        )
        db.add(order_item)

    # Clear the user's cart
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()

    db.commit()
    return {"message": "Order placed successfully", "order_id": order.id}

@router.get("/orders")
def view_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return [
        {
            "order_id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at,
        }
        for order in orders
    ]
