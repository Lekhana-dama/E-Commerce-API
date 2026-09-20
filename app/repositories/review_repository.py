
from sqlalchemy.orm import Session
from app.models.review import Review

class ReviewRepository:
    @staticmethod
    def create(db:Session,user_id:int,product_id:int,rating:int,comment:str|None):
        review=Review(user_id=user_id,product_id=product_id,rating=rating,comment=comment)
        db.add(review)
        db.commit()
        db.refresh(review)
    @staticmethod
    def get_by_product(db:Session,product_id:int):
        return db.query(Review).filter(Review.product_id==product_id).all()
    @staticmethod
    def get_by_id(db:Session,review_id:int):
        return db.query(Review).filter(Review.id==review_id).first()
    @staticmethod
    def get_by_user_and_product(db:Session,user_id:int,product_id:int):
        return db.query(Review.user_id==user_id,Review.product_id==product_id).first()
    @staticmethod
    def update(db:Session,review:Review,rating:int,comment:str|None):
        review.rating=rating
        review.comment=comment
        db.commit()
        db.refresh(review)
        return review
    @staticmethod
    def delete(db:Session,review:Review):
        db.delete(review)
        db.commit()