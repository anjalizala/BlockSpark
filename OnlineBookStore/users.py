from fastapi import FastAPI,HTTPException,APIRouter
from sqlalchemy.orm import Session
import model,auth
from database import sessionLocal
from datetime import timedelta,datetime
import books
#from model import User

router = APIRouter()

@router.post("/register")
def register(name:str, email:str, password:str):
    db = sessionLocal()
    hashed_password = auth.get_password_hash(password)
    db_user = model.User(name=name,email=email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"User registered successfully"}

@router.post("/login")
def login(email:str, password:str):
    db = sessionLocal()
    db_user = db.query(model.User).filter(model.User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid Email")

    if not auth.verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    db_user.last_login = datetime.utcnow()
    db.commit()
            
    role = "admin" if db_user.is_admin else "user"
    access_token = auth.create_access_token({"sub": db_user.name,"role": role})
    return {"access_token": access_token, "token_type": "bearer","message": "Login Successfull"}
    
    
     