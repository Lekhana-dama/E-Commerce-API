from app.schemas.products import ProductCreate
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class ProductService:
    @staticmethod
    def create_product(db:Session,product_data:ProductCreate):
        #check whether category exists or not
        category=CategoryRepository.get_by_id(db,product_data.category_id)
        if not category:
            raise ValueError("category not found")
        #duplicated product
        existing_product=ProductRepository.get_by_name(db,product_data.name)
        if existing_product :
            raise ValueError("product already exists")
        if product_data.price<=0:
            raise ValueError("price must be greater than 0")
        if product_data.stock_quantity <0:
            raise ValueError("Stock quantity cannot be negative")
        return ProductRepository.create(db,name=product_data.name,description=product_data.description,price=product_data.price,stock_quantity=product_data.stock_quantity,category_id=product_data.category_id,image_url=product_data.image_url)
    @staticmethod
    def get_all_products(db:Session):
        return ProductRepository.get_all(db)
    @staticmethod
    def get_product_by_id(db:Session,product_id:int):
        product =ProductRepository.get_by_id(db,product_id)
        if not product:
            raise ValueError("Product not found")
        return product
    @staticmethod
    def get_product_by_name(db:Session,name:str):
        prduct=ProductRepository.get_by_name(db,name)
        if not prduct:
            return ValueError("Product not found")
        return prduct
    @staticmethod
    def update(db:Session,product_id:int,product_data:ProductCreate):
        product=ProductRepository.get_by_id(db,product_id)
        if not product:
            raise ValueError("product not found")
        cat=CategoryRepository.get_by_id(db,product_data.category_id)
        if not cat:
            raise ValueError("category not found")
        exisiting_product=ProductRepository.get_by_name(db,product.name)
        if exisiting_product and exisiting_product.id !=product_id:
            raise ValueError("Product name already exists")
        if product_data.price<=0:
            raise ValueError("Price must be greater than 0")
        if product_data.stock_quantity <0:
            raise ValueError("Products can't be negitive")
        return ProductRepository.update(db=db,product=product,name=product_data.name,description=product_data.description,price=product_data.price,stock_quantity=product_data.stock_quantity,category_id=product_data.category_id,image_url=product_data.image_url)
    
    @staticmethod
    def delete_product(db:Session,product_id:int):
        product=ProductRepository.get_by_id(db,product_id)
        if not product:
            raise ValueError("product not found")
        ProductRepository.delete(db,product)


