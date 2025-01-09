from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from database import sessionLocal
import model

SECRET_KEY = "8435807f2d1abda2316b17452f62fba9aa713229a4e1b1cb36ae91bddf87a07f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=365*ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

admin_data = {"sub": "admin_user", "role": "admin"}
token = create_access_token(admin_data)
print(f"Admin token: {token}")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
