from core.database import SessionLocal,get_db
from .auth_models import User
from .auth_schemas import UserCreate,UserRead,UserLogin
from core import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    try:
        new_db_user = User(
            username=user.username,
            email=user.email,
            hashpassword=hash_password(user.password))
        db.add(new_db_user)
        db.commit()
        db.refresh(new_db_user)
        return new_db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error in def create_user, error: {e}')

def verify_user_exists(db: Session, user: UserCreate):
       try:
        stmt = db.query(User).filter(User.username == user.username and User.email == user.email).first()
        if not stmt:
            return False
        return True
       except Exception as e:
           raise HTTPException(status_code=500, detail='Error in def verify_user_exists, error: {e}')
       

       