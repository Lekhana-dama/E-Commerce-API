from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate

class CategoryService:
    @staticmethod
    def create_category(db:Session,category_data:CategoryCreate):
        exisiting_category=CategoryRepository.get_by_name(db,category_data.name)
        if exisiting_category :
            raise ValueError("Category already exists")
        return CategoryRepository.create(db=db,name=category_data.name,description=category_data.description)
    @staticmethod
    def get_all_categories(db:Session):
        return CategoryRepository.get_all(db)
    @staticmethod
    def get_category_by_id(db:Session,category_id:int):
        category=CategoryRepository.get_by_id(db,category_id)
        if not category:
            raise ValueError("Category not found")
        return category
    @staticmethod
    def update_category(db:Session,category_id:int,category_data:CategoryCreate):
        category=CategoryRepository.get_by_id(db,category_id)
        if not category:
            raise ValueError("Category not found")
        existing_category=CategoryRepository.get_by_name(db,category_data.name)
        if existing_category and existing_category.id != category_id:
            raise ValueError("Category name already exists")

        return CategoryRepository.update(
            db=db,
            category=category,
            name=category_data.name,
            description=category_data.description
        )

    @staticmethod
    def delete_category(
        db: Session,
        category_id: int
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id
        )

        if not category:
            raise ValueError("Category not found")

        CategoryRepository.delete(
            db,
            category
        )