from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.repositories.order_repository import OrderRepository
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.orders import OrderCreate


class OrderService:
    @staticmethod
    def create_order(
        db: Session,
        user_id: int,
        order_data: OrderCreate
    ):
        try:

            # 1. Get user's cart
            cart = CartRepository.get_by_user(
                db,
                user_id
            )

            if not cart:
                raise ValueError("Cart not found")

            # 2. Get cart items
            cart_items = db.query(CartItem).filter(
                CartItem.cart_id == cart.id
            ).all()

            if not cart_items:
                raise ValueError("Cart is empty")

            total_amount = 0

            # 3. Validate products and calculate total
            for item in cart_items:

                product = ProductRepository.get_by_id(
                    db,
                    item.product_id
                )

                if not product:
                    raise ValueError("Product not found")

                if not product.is_active:
                    raise ValueError(
                        f"Product {product.name} is not available"
                    )

                if item.quantity > product.stock_quantity:
                    raise ValueError(
                        f"Insufficient stock for {product.name}"
                    )

                subtotal = product.price * item.quantity

                total_amount += subtotal

            # 4. Create order
            order = OrderRepository.create_order(
                db=db,
                user_id=user_id,
                status="PENDING",
                total_amount=total_amount,
                shipping_address=order_data.shipping_address
            )

            # 5. Create order items and reduce stock
            for item in cart_items:

                product = ProductRepository.get_by_id(
                    db,
                    item.product_id
                )

                subtotal = product.price * item.quantity

                OrderRepository.create_order_item(
                    db=db,
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    price=product.price,
                    quantity=item.quantity,
                    subtotal=subtotal
                )

                # Reduce product stock
                product.stock_quantity -= item.quantity

            # 6. Clear cart
            for item in cart_items:
                CartRepository.delete_item(
                    db,
                    item
                )

            # 7. Commit everything together
            db.commit()

            db.refresh(order)

            return order

        except Exception:

            # Undo all database changes if anything fails
            db.rollback()

            # Send the error to the caller
            raise
    @staticmethod
    def get_user_order(db:Session,user_id:int):
                        order=OrderRepository.get_by_user(db,user_id)
                        return order
    @staticmethod
    def cancel_order(
    db: Session,
    user_id: int,
    order_id: int
):
        order = OrderRepository.get_by_id(
            db,
            order_id
        )

        if not order:
            raise ValueError("Order not found")

        if order.user_id != user_id:
            raise ValueError("You cannot cancel this order")

        if order.status != "PENDING":
            raise ValueError("Only pending orders can be cancelled")

        order.status = "CANCELLED"

        db.commit()
        db.refresh(order)

        return order