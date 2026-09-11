from sqlalchemy import Column,Text,String,Integer,Boolean,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False,unique=True,index=True)
    description=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    products=relationship("Product",back_populates="category")