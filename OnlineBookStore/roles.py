from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import sessionLocal
from jose import jwt, JWTError
from model import User
from auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()
SECRET_KEY = "8435807f2d1abda2316b17452f62fba9aa713229a4e1b1cb36ae91bddf87a07f"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(sessionLocal)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/protected/user")
def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/protected/admin")
def admin_endpoint(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": f"Hello, {current_user['name']}! You are an admin."}


# from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.auth import decode_jwt_token  # Helper to decode JWT token

# def is_admin(token: str = Depends(decode_jwt_token), db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == token["sub"]).first()
#     if not user or user.type != "admin":
#         raise HTTPException(status_code=403, detail="Access forbidden")
#     return user
