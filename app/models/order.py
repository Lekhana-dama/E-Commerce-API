from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text
)
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    shipping_address = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")