
from sqlalchemy import Column,Integer,Text,DateTime,ForeignKey,UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class Review(Base):
    __tablename__="reviews"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False,index=True)
    rating=Column(Integer,nullable=False)
    comment=Column(Text,nullable=True)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    user=relationship("User",back_populates="reviews")
    product=relationship("Product",back_populates="reviews")
    __table_args__=(
        UniqueConstraint(
            "user_id","product_id",name="uq_user_product_review"
            ),
        )
