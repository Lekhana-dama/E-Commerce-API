from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.repositories.review_repository import ReviewRepository
from app.models.order import Order
from app.models.order_items import OrderItem
from app.schemas.review import ReviewCreate

class ReviewService:
    @staticmethod
    def create_review(db:Session,user_id:int,review_data:ReviewCreate):
        #checking whether the product exisits
        existing_product=ProductRepository.get_by_id(db,review_data.product_id)
        if not existing_product:
            raise ValueError("product not found")
        #checking whether the user has already reviewed  the product
        existing_review=(ReviewRepository.get_by_user_and_product(db,user_id,review_data.product_id))
        if existing_review:
            raise ValueError("You have alreday reviwed this product")
        #checking whether the user purchased the product
        purchased_product=(db.query(OrderItem).join(Order).filter(Order.user_id==user_id,OrderItem.product_id==review_data.product_id,Order.status=="DELIVERED").first())
        if not purchased_product:
            raise ValueError("You can review only purchased products")
        return ReviewRepository.create(
            db=db,user_id=user_id,product_id=review_data.product_id,rating=review_data.rating,comment=review_data.comment
        )
    @staticmethod 
    def get_product_reviews(db:Session,product_id:int):
        product=ProductRepository.get_by_id(db,product_id)
        if not product:
            raise ValueError ("Product not found")
        return ReviewRepository.get_by_product(db,product_id)

    @staticmethod
    def update_review(db:Session,user_id:int,review_id:int,rating:int,comment:str|None):
        review=ReviewRepository.get_by_id(db,review_id)
        if not review:
            raise ValueError("Review not found")
        if review.user_id !=user_id:
            raise ValueError("you can update only yourn own review")
        return ReviewRepository.update(db=db,review=review,rating=rating,comment=comment)
    @staticmethod
    def delete_review(db:Session,user_id:int,review_id:int):
        review=ReviewRepository.get_by_id(db,review_id)
        if not review:
            raise ValueError("Review not found")

        if review.user_id != user_id:
            raise ValueError(
                "You can delete only your own review"
            )

        ReviewRepository.delete(db,review)
        return {
            "message":"Review deleted successfully"
        }
