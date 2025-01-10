from fastapi import Depends, HTTPException, status , APIRouter
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import User
from schemas import UserCreate, Token, UserOut
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordRequestForm
from auth import get_user, get_password_hash, get_current_user, create_access_token, authenticate_user

router = APIRouter()

@router.post("/register",response_model = UserOut , tags=['Register'])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
        
    password = get_password_hash(user.password)
    
    new_user = User(username=user.username, email=user.email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", tags=['User'])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_form = authenticate_user(db, form_data.username, form_data.password)
    #user = authenticate_user(db, username, password)
    if not user_form :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = db.query(User).filter(User.username==form_data.username).first()
    
    if db_user.type == "1":
        role = "admin"
    else:
        role = "user"
    access_token = create_access_token({"sub": user_form.username, "role": role})
    return { "access_token": access_token, "token_type": "bearer","message": "Login Successful", "role": role}
        
@router.get("/users/me", response_model = UserOut,  tags=['User'])
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
    
    
    
    
    
