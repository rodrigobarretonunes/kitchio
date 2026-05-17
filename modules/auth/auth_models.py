from sqlalchemy import Column, Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "kitchio_users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hash_password = Column(String, nullable = False)
    created_at = Column(DateTime)
    role = Column(String, default="U") # U: User, A:Admin/SuperUser
    is_active = Column(Boolean, default=True)

