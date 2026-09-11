from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cart_item import CartItem


class CartRepository:

    @staticmethod
    def get_by_user(db:Session,user_id:int):
        return db.query(Cart).filter(Cart.user_id==user_id).first()
    @staticmethod
    def create(db:Session,user_id:int):
        cart=Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def get_item(db:Session,card_id:int,product_id:int):
        return db.query(CartItem).filter(CartItem.cart_id==card_id,CartItem.product_id==product_id).first()
    @staticmethod
    def get_item_by_id(db: Session, item_id: int):
        return db.query(CartItem).filter(
            CartItem.id == item_id
        ).first()
    @staticmethod
    def create_item(db:Session,cart_id:int,product_id:int,quantity:int):
        cart_itrm=CartItem(cart_id=cart_id,product_id=product_id,quantity=quantity)
        db.add(cart_itrm)
        db.commit()
        db.refresh(cart_itrm)
        return cart_itrm
    @staticmethod
    def update_item(db:Session,cart_item:CartItem,quantity:int):
        cart_item.quantity=quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item

    @staticmethod
    def delete_item(db:Session,cart_item:CartItem):
        db.delete(cart_item)
        db.commit()








        




