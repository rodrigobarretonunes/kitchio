from passlib.context import CryptContext
from dotenv import load_dotenv
import os 
import logging
from jose import jwt
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

#================= Password Hashing and Verification =================#
def hash_password(password:str):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

#================= JWT Token Generation and Verification =================#

def create_token(user_db):
    payload = {
        "sub": user_db.id,
        "username":user_db.username,
        "role": user_db.role
    }
    SECRET_KEY = os.getenv("SECRET_KEY")

    try:
        token = jwt.encode(payload,SECRET_KEY, algorithm="HS256")
        if token: 
            logging.info(f"Token created successfully for user: {user_db.username}")
            return token
        else: 
            return None
    except Exception as e:
        logging.error(f'Error in create_token: {e}')
        raise HTTPException(status_code=500, detail=f'Error in create_token: {e}')
    
def verify_token(token:str):
    SECRET_KEY = os.getenv("SECRET_KEY")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logging.warning("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        logging.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

# In the future this function will be replace in another module called auth_dependencies.
def get_current_user(token:str):
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        username = payload.get("username")
        role = payload.get("role")
        if user_id is None or username is None:
            logging.warning("Invalid token payload")
            raise HTTPException(status_code=401, detail="Invalid token payload")
        else:
            logging.info(f"Token verified successfully for user: {username}")
            return {"user_id": user_id, "username": username, "role": role}
    except HTTPException as e:
        raise e