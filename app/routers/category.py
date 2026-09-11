from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.authorization import require_admin
from app.schemas.category import CategoryCreate,CategoryResponse
from app.services.category_service import CategoryService

router=APIRouter(prefix="/categories",tags=["Categories"])
@router.post("",response_model=CategoryResponse)
def create_category(category_data:CategoryCreate,db:Session=Depends(get_db),current_admin=Depends(require_admin)):
    try:
        return CategoryService.create_category(db,category_data)
    except Exception as e:
        raise HTTPException(status_code=404,detail="value error")

@router.get("",response_model=list[CategoryResponse])
def get_categories(db:Session=Depends(get_db)):
    return CategoryService.get_all_categories(db)

@router.get("/{category_id}",response_model=CategoryResponse)
def get_category(category_id:int,db:Session=Depends(get_db)):
    try:
        return CategoryService.get_category_by_id(db,category_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.put("/{category_id}",response_model=CategoryResponse)
def update_category(category_id:int,category_data:CategoryCreate,db:Session=Depends(get_db),current_admin=Depends(require_admin)):
    try:
        return CategoryService.update_category(db,category_id,category_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)
):
    try:
        CategoryService.delete_category(
            db,
            category_id
        )

        return {
            "message": "Category deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )   