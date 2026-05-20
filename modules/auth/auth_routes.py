from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from . import create_user, verify_user_exists,get_user_by_username,UserCreate, UserRead, UserLogin
from core.security import verify_password, create_token



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if verify_user_exists(db, user):
        raise HTTPException(status_code=400, detail="User already exists")
    else: new_user = create_user(db, user)
    return new_user

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db,user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail='Invalid username')
    if not verify_password(user.password, db_user.hash_password):
        raise HTTPException(status_code=400, detail='Invalid password')
    else:
        if token :=create_token(db_user):
            raise HTTPException(status_code=200, detail={"access_token": token})

            
        




    
    
    