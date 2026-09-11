from sqlalchemy.orm import Session
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartCreate

class CartService:
    @staticmethod
    def get_cart(db:Session,user_id:int):
        cart=CartRepository.get_by_user(db,user_id)
        if not cart:
            cart=CartRepository.create(db,user_id)
        return cart
    @staticmethod
    def add_to_cart(db:Session,user_id:int,cart_item:CartCreate):
        if cart_item.quantity<=0:
            raise ValueError("Quantity must be greater than 0")
        product=ProductRepository.get_by_id(db,cart_item.product_id)
        if not product:
            raise ValueError("product not found")
        if not product.is_active:
            raise ValueError("Product is not available")
        if cart_item.quantity > product.stock_quantity:
            raise ValueError("Insufficient stock")
        cart=CartRepository.get_by_user(db,user_id)
        existing_item=CartRepository.get_item(db,cart.id,cart_item.product_id)
        if existing_item:

            new_quantity = (
                existing_item.quantity
                + cart_item.quantity
            )

            if new_quantity > product.stock_quantity:
                raise ValueError("Insufficient stock")

            return CartRepository.update_item(
                db,
                existing_item,
                new_quantity
            )

        return CartRepository.create_item(
            db=db,
            cart_id=cart.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )

    @staticmethod
    def update_cart_item(
        db: Session,
        user_id: int,
        item_id: int,
        quantity: int
    ):

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        cart = CartRepository.get_by_user(db, user_id)

        if not cart:
            raise ValueError("Cart not found")
        cart_item = CartRepository.get_item_by_id(
            db,
            item_id
        )

        if not cart_item or cart_item.cart_id != cart.id:
            raise ValueError("Cart item not found")

        product = ProductRepository.get_by_id(
            db,
            cart_item.product_id
        )

        if not product:
            raise ValueError("Product not found")

        if quantity > product.stock_quantity:
            raise ValueError("Insufficient stock")

        return CartRepository.update_item(
            db,
            cart_item,
            quantity
        )

    @staticmethod
    def remove_cart_item(
        db: Session,
        user_id: int,
        item_id: int
    ):

        cart = CartRepository.get_by_user(db, user_id)

        if not cart:
            raise ValueError("Cart not found")

        cart_item = CartRepository.get_item_by_id(
            db,
            item_id
        )

        if not cart_item or cart_item.cart_id != cart.id:
            raise ValueError("Cart item not found")

        CartRepository.delete_item(
            db,
            cart_item
        )

        return {"message": "Cart item removed successfully"}