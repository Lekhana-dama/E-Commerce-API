from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepository:
    @staticmethod
    def create(db:Session,name:str,description:str|None,price:float,stock_quantity:int,category_id:int,image_url:str|None):
        product=Product(name=name,description=description,price=price,stock_quantity=stock_quantity,category_id=category_id,image_url=image_url)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    @staticmethod
    def get_all(db:Session):
        return db.query(Product).all()

    @staticmethod
    def get_by_id(db:Session,product_id:int):
        return db.query(Product).filter(Product.id==product_id).first()
    @staticmethod
    def get_by_name(db:Session,product_name:int):
        return db.query(Product).filter(Product.name==product_name).first()

    @staticmethod
    def update(db:Session,product:Product,name:str,description:str|None,price:float,stock_quantity:int,category_id:int,image_url:str|None):
        product.name=name
        product.description=description
        product.price=price
        product.stock_quantity=stock_quantity
        product.category_id=category_id
        product.image_url=image_url

        db.commit()
        db.refresh(product)
        return product
    @staticmethod
    def delete(db:Session,product:Product):
        db.delete(product)
        db.commit()
    