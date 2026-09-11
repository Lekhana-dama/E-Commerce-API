from sqlalchemy import Column,Integer,String,Boolean,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False,index=True)
    password_hash=Column(String(255),nullable=False)
    role=Column(String(20),nullable=False,default="CUSTOMER")
    is_active=Column(Boolean,nullable=False,default=True)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    orders=relationship("Order",back_populates="user")
    cart=relationship("Cart",back_populates="user",uselist=False)

