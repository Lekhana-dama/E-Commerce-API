from app.services.product_service import ProductService
from sqlalchemy.orm import Session
from app.dependencies.authorization import require_admin
from app.dependencies.database import get_db
from app.schemas.products import ProductCreate,ProductResponse
from fastapi import APIRouter,Depends,HTTPException

router=APIRouter(prefix="/products",tags=["Products"])

@router.post("",response_model=ProductResponse)
def create_product(product_data:ProductCreate,db:Session=Depends(get_db),current_admin=Depends(require_admin)):
    try:
        return ProductService.create_product(db,product_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.get("",response_model=list[ProductResponse])
def get_products(db:Session=Depends(get_db)):
    return ProductService.get_all_products(db)

@router.get("/{product_id}",response_model=ProductResponse)
def get_products_by_id(product_id:int,db:Session=Depends(get_db)):
    try:
        return ProductService.get_product_by_id(db,product_id=product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.get("/name/{name}",response_model=ProductResponse)
def get_by_name(name:str,db:Session=Depends(get_db)):
    try:
        return ProductService.get_product_by_name(
            db,
            name
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.put("/{product_id}",response_model=ProductResponse)
def update(product_id:int,product_data:ProductCreate,db:Session=Depends(get_db),current_admin=Depends(require_admin)):
    try:
        return ProductService.update(db,product_id,product_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db),current_admin=Depends(require_admin)):
    try:
        ProductService.delete_product(db,product_id)
        return{"message":"Product deleted sucessflly"}
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )