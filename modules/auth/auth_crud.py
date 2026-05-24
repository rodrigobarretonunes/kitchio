from .auth_models import User
from .auth_schemas import UserCreate, UserRead, UserLogin
from core import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone
import logging


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
        stmt_username = db.query(User).filter((User.username == user.username)).first()
        if stmt_username:
            print("User already exists")
            return True
        if stmt_email := db.query(User).filter((User.email == user.email)).first():
            print("Email already exists")
            return True
        else:
            print("User does not exist")
            return False
       except Exception as e:
           raise HTTPException(status_code=500, detail='Error in def verify_user_exists, error: {e}')
       

def get_user_by_username(db: Session, username:str):
    try:
        stmt = db.query(User).filter(User.username == username).first()
        if stmt:
            logging.info(f"User found: {stmt.username}")
            return stmt
        else:
            logging.info(f'User not found with username: {username}')
            return None
    except Exception as e:
        logging.error(f'Error in get_user_by_username: {e}')
        raise HTTPException(status_code=500, detail=f'Error in get_user_by_username: {e}')
    
def change_status_user(db: Session, username: str):
        stmt = db.query(User).filter(User.username == username).first()
        try:
            if stmt and stmt.is_active:
                stmt.is_active = False
                stmt.date_status_changed = datetime.now(timezone.utc)
                db.commit()
                logging.info(f'User {username} deactivated successfully')
            elif stmt and not stmt.is_active:
                stmt.is_active = True
                stmt.date_status_changed = datetime.now(timezone.utc)
                db.commit()
                logging.info(f'User {username} activated successfully')
            else:
                logging.warning(f'User not found with username: {username}')
                raise HTTPException(status_code=404, detail=f'User not found with username: {username}')
        except Exception as e:
            logging.error(f'Error in change_status_user: {e}')
            raise HTTPException(status_code=500, detail=f'Error in change_status_user: {e}')