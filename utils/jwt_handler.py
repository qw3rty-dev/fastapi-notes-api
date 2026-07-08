import jwt
from database import get_db
from models import User
from utils.password import verify_password,hash_password
from datetime import datetime,UTC,timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/users/login")

def create_token_access(user_id:int)->str:
    expire = datetime.now(UTC) + timedelta(30)
    payload = {
        "sub": str(user_id),
        "exp":expire
    }    
    return jwt.encode(
        payload,
        algorithm= ALGORITHM,
        key= SECRET_KEY)

def verify_token_access(token:str)->int:
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Unauthorized")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401,detail="Unauthorized")
    user_id = int(sub)

    return user_id


def get_current_user(token:str= Depends(oauth2_scheme),
                     db:Session= Depends(get_db))->User:
    current_user_id = verify_token_access(token)
    current_user= db.scalar(select(User).where(User.id == current_user_id))
    if not current_user:
       raise HTTPException(status_code= 401,detail="Invalid authentication credentials")
    return current_user