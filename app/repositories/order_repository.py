from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_items import OrderItem


class OrderRepository:

    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        status: str,
        total_amount: float,
        shipping_address: str
    ):
        order = Order(
            user_id=user_id,
            status=status,
            total_amount=total_amount,
            shipping_address=shipping_address
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    @staticmethod
    def create_order_item(
        db: Session,
        order_id: int,
        product_id: int,
        product_name: str,
        price: float,
        quantity: int,
        subtotal: float
    ):
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            price=price,
            quantity=quantity,
            subtotal=subtotal
        )

        db.add(order_item)
        db.commit()
        db.refresh(order_item)

        return order_item

   

    @staticmethod
    def get_by_id(db: Session, order_id: int):
        return db.query(Order).filter(
            Order.id == order_id
        ).first()

    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return db.query(Order).filter(
            Order.user_id == user_id
        ).all()

    @staticmethod
    def get_items(db: Session, order_id: int):
        return db.query(OrderItem).filter(
            OrderItem.order_id == order_id
        ).all()

    @staticmethod
    def update_status(db: Session, order: Order, status: str):
        order.status = status

        db.commit()
        db.refresh(order)

        return order