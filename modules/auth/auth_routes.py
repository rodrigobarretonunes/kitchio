from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from auth import create_user, verify_user_exists, UserCreate, UserRead, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if verify_user_exists(user):
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(db, user)
    return new_user



    
    
    