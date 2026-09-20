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
    def search_products(db:Session,search:str):
        return ProductRepository.search_products(db,search)
    
    @staticmethod
    def get_paginated_products(
        db: Session,
        page: int,
        limit: int
    ):
        if page < 1:
            raise ValueError(
                "Page must be greater than 0"
            )

        if limit < 1 or limit > 100:
            raise ValueError(
                "Limit must be between 1 and 100"
            )

        return ProductRepository.get_paginated_products(
            db,
            page,
            limit
        )
        
    @staticmethod
    def sort_products(
        db: Session,
        sort_by: str = "id",
        order: str = "asc"
    ):
        allowed_sort_fields = ["id", "price", "name"]
        allowed_orders = ["asc", "desc"]

        if sort_by not in allowed_sort_fields:
            raise ValueError(
                "Invalid sorting field"
            )

        if order not in allowed_orders:
            raise ValueError(
                "Invalid sorting order"
            )

        return ProductRepository.sort_products(
            db,
        sort_by,
        order
    )
    @staticmethod
    def filter_products(
        db: Session,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None
    ):
        if min_price is not None and min_price < 0:
            raise ValueError(
                "Minimum price cannot be negative"
            )

        if max_price is not None and max_price < 0:
            raise ValueError(
                "Maximum price cannot be negative"
            )

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise ValueError(
                "Minimum price cannot be greater than maximum price"
            )

        return ProductRepository.filter_products(
            db,
            category_id,
            min_price,
            max_price
        )
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
        if page < 1:
            raise ValueError("Page must be greater than 0")

        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        if min_price is not None and min_price < 0:
            raise ValueError("Minimum price cannot be negative")

        if max_price is not None and max_price < 0:
            raise ValueError("Maximum price cannot be negative")

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise ValueError("Minimum price cannot exceed maximum price")

        if sort_by not in ["id", "name", "price"]:
            raise ValueError("Invalid sort field")

        if order not in ["asc", "desc"]:
            raise ValueError("Invalid sort order")

        return ProductRepository.browse_products(
            db=db,
            search=search,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            order=order,
            page=page,
            limit=limit
        )
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


