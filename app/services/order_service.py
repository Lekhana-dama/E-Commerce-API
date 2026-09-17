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
        # 1. Get user's cart
        cart = CartRepository.get_by_user(db, user_id)

        if not cart:
            raise ValueError("Cart not found")

        # 2. Get cart items
        cart_items = db.query(CartItem).filter(
            CartItem.cart_id == cart.id
        ).all()

        if not cart_items:
            raise ValueError("Cart is empty")

        # 3. Calculate total
        total_amount = 0

        for item in cart_items:

            # Get product
            product = ProductRepository.get_by_id(
                db,
                item.product_id
            )

            if not product:
                raise ValueError("Product not found")

            # Check product availability
            if not product.is_active:
                raise ValueError(
                    f"Product {product.name} is not available"
                )

            # Check stock
            if item.quantity > product.stock_quantity:
                raise ValueError(
                    f"Insufficient stock for {product.name}"
                )

            # Calculate subtotal
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
       
        # 5. Create order items
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

            # 6. Reduce stock
            product.stock_quantity -= item.quantity

        db.commit()

        # 7. Clear cart
        for item in cart_items:
            CartRepository.delete_item(db, item)

        return order
    @staticmethod
    def get_user_order(db:Session,user_id:int):
                    order=OrderRepository.get_by_user(db,user_id)
                    return order