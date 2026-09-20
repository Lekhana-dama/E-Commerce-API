from sqlalchemy import Column,String,ForeignKey,Integer,Text,Numeric,Boolean,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class Product(Base):
    __tablename__="products"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(Text,nullable=True)
    price=Column(Numeric(10,2),nullable=False)
    stock_quantity=Column(Integer,default=0,nullable=False)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False,index=True)
    is_active=Column(Boolean,nullable=False,default=True)
    image_url=Column(String,nullable=True)

    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    reviews=relationship("Review",back_populates="product")