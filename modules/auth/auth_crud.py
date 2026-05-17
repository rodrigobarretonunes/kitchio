from .auth_models import User
from .auth_schemas import UserCreate, UserRead, UserLogin
from core import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone


def create_user(db: Session, user:UserCreate):
    try:
        new_db_user = User(
            username=user.username,
            email=user.email,
            hash_password=hash_password(user.password),
            created_at=datetime.now(timezone.utc),
            role="U",
            is_active=True)
        
        db.add(new_db_user)
        db.commit()
        db.refresh(new_db_user)
        return new_db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def verify_user_exists(db:Session, user: UserCreate):
       try:
        stmt = db.query(User).filter((User.username == user.username) & (User.email == user.email)).first()
        if stmt:
            print("User already exists")
            return True
        else:
            print("User does not exist")
            return False
       except Exception as e:
           raise HTTPException(status_code=500, detail='Error in def verify_user_exists, error: {e}')
       

       