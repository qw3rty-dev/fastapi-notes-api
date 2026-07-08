from fastapi import Depends,HTTPException,APIRouter
from utils.password import hash_password,verify_password
from utils.jwt_handler import create_token_access,get_current_user
from database import get_db
from models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime,UTC
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserRegister,UserResponse,TokenResponse


router = APIRouter(prefix="/users",tags=["Users"])


@router.post("/register",response_model= UserResponse)
def register(user:UserRegister,
             db:Session= Depends(get_db)):
    new_user = User(
        username= user.username,
        email = user.email,
        hashed_password = hash_password(user.password)
    )
    try: 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code= 409,detail = "User already exists")
    return new_user
    
    

@router.post("/login",response_model= TokenResponse)
def login(db:Session= Depends(get_db),
          form_data:OAuth2PasswordRequestForm =Depends()):
    user = db.scalar(select(User).where(User.email == form_data.username))
    
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail= "Invalid authentication credentials")
    user.last_login = datetime.now(UTC)
    db.commit()
    token = create_token_access(user.id)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me",response_model=UserResponse)
def get_me(current_user : User = Depends(get_current_user)):
    return current_user