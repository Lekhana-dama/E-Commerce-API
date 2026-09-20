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
    def search_products(db:Session,search:str):
        return db.query(Product).filter(Product.name.ilike(f"{search}")).all()
    @staticmethod
    def filter_products(db:Session,
                        category_id:int|None=None,
                        min_price:float|None=None,
                        max_price:float|None=None):
        query=db.query(Product)
        if category_id is not None:
            query=db.filter(Product.category_id==category_id)
        if min_price is not None:
            query=query.filter(Product.price>=min_price)

        if max_price is not None:
            query=query.filter(Product.price<=max_price)
        return query.all()
        
    @staticmethod
    def sort_products(
        db: Session,
        sort_by: str = "id",
        order: str = "asc"
    ):
        query = db.query(Product)

        if sort_by == "price":
            sort_column = Product.price

        elif sort_by == "name":
            sort_column = Product.name

        else:
            sort_column = Product.id

        if order == "desc":
            query = query.order_by(
                sort_column.desc()
            )
        else:
            query = query.order_by(
                sort_column.asc()
            )

        return query.all()
    @staticmethod
    def get_pagination_products(db:Session,page:int,limit:int):
        offset=(page-1)*limit
        return db.query(Product).offset(offset).limit(limit).all()
    @staticmethod
    def get_by_id(db:Session,product_id:int):
        return db.query(Product).filter(Product.id==product_id).first()
    @staticmethod
    def get_by_name(db:Session,product_name:int):
        return db.query(Product).filter(Product.name==product_name).first()
    @staticmethod
    def browse_products(
        db: Session,
        search: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "id",
        order: str = "asc",
        page: int = 1,
        limit: int = 10
    ):
        query = db.query(Product)

        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))

        if category_id is not None:
            query = query.filter(Product.category_id == category_id)

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        total = query.count()

        if sort_by == "price":
            sort_column = Product.price
        elif sort_by == "name":
            sort_column = Product.name
        else:
            sort_column = Product.id

        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        offset = (page - 1) * limit

        products = query.offset(offset).limit(limit).all()

        return products, total
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
    