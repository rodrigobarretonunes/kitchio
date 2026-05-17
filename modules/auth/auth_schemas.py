from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    id : int 
    username: str
    email: str
    status: bool = True
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str



