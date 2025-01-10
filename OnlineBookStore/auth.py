from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


#JWT KEY 
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS= 2

#password 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Authantication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#verify the password matches a hased password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#generate hash password
def get_password_hash(password):
    return pwd_context.hash(password)

#jwt token created
def create_access_token(data: dict):
    to_encode = data.copy()  # Create a copy to avoid modifying the original dictionary
    expire = datetime.utcnow() + timedelta(days=365*ACCESS_TOKEN_EXPIRE_DAYS)  # Use days directly
    to_encode.update({"exp": expire})  # Add expiration to the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#get data from database user
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

#authenticates user by verify user and password 
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

#get user verify and provid token from database

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    # Attach role to the user object
    user.role = role
    return user

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None