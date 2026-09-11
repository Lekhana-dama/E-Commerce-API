from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    @staticmethod
    def create(db:Session,name:str,description:str|None=None):
        category=Category(name=name,description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_all(db:Session):
        return db.query(Category).all()

    @staticmethod
    def get_by_id(db:Session,category_id:int):
        return db.query(Category).filter(Category.id==category_id).first()

    @staticmethod
    def get_by_name(db:Session,name:int):
        return db.query(Category).filter(Category.name==name).first()

    @staticmethod
    def update(db:Session,category:Category,name:str,description:str|None):
        category.name=name
        category.description=description
        db.commit()
        db.refresh(category)
        return category
    @staticmethod
    def delete(db:Session,category:Category):
        db.delete(category)
        db.commit()