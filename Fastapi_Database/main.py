from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import User, SessionLocal

app = FastAPI()

# Create a new user
@app.post("/users/")
def create_user(name: str, email: str):
    db = SessionLocal()  # Explicitly create a session
    try:
        db_user = db.query(User).filter(User.email == email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(name=name, email=email)
        db.add(new_user)
        db.commit()
        return new_user
    finally:
        db.close()  # Close the session

# Get all users
@app.get("/users/")
def get_users():
    db = SessionLocal()  # Explicitly create a session
    try:
        return db.query(User).all()
    finally:
        db.close()  # Close the session

# Get a user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = SessionLocal()  # Explicitly create a session
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()  # Close the session

# Update a user
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str):
    db = SessionLocal()  # Explicitly create a session
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.name = name
        user.email = email
        db.commit()
        return user
    finally:
        db.close()  # Close the session

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()  # Explicitly create a session
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    finally:
        db.close()  # Close the session
