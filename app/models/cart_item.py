from sqlalchemy import Column,Integer,DateTime,String,ForeignKey,UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class CartItem(Base):
    __tablename__="cart_items"
    id=Column(Integer,primary_key=True,index=True)
    cart_id=Column(Integer,ForeignKey("carts.id"),nullable=False,index=True)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False,index=True)
    quantity=Column(Integer,default=1,nullable=False)
    created_on=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_on=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    __table_args__=(
        UniqueConstraint("cart_id","product_id",name="uq_cart_product"),
    )
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")