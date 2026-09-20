from app.services.product_service import ProductService
from sqlalchemy.orm import Session
from app.dependencies.authorization import require_admin
from app.dependencies.database import get_db
from app.schemas.products import ProductCreate,ProductResponse,ProductListResponse
from fastapi import APIRouter,Depends,HTTPException
from app.core.redis_client import redis_client
from fastapi.encoders import jsonable_encoder
import json

router=APIRouter(prefix="/products",tags=["Products"])

@router.post("", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin)
):
    try:
        product = ProductService.create_product(db, product_data)

        # Clear old product cache
        redis_client.delete("products:all")

        return product

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):

    cache_key = "products:all"
    cached_products = None

    try:
        cached_products = redis_client.get(cache_key)
    except Exception as e:
        print(f"Redis unavailable: {e}")

    if cached_products:
        print("CACHE HIT")
        return json.loads(cached_products)

    print("CACHE MISS")

    products = ProductService.get_all_products(db)
    products_data = jsonable_encoder(products)

    try:
        redis_client.setex(
            cache_key,
            60,
            json.dumps(products_data)
        )
    except Exception as e:
        print(f"Redis cache save failed: {e}")

    return products

@router.get("/search",response_model=list[ProductResponse])
def search_products(search:str,db:Session=Depends(get_db)):
    return ProductService.search_products(db,search)
@router.get("/page",response_model=list[ProductResponse])
def pagination(page:int=1,limit:int=10,db:Session=Depends(get_db)):
    try:
        return ProductService.get_paginated_products(db,page,limit)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get(
    "/filter",
    response_model=list[ProductResponse]
)
def filter_products(
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    try:
        return ProductService.filter_products(
            db,
            category_id,
            min_price,
            max_price
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "/sort",
    response_model=list[ProductResponse]
)
def sort_products(
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    try:
        return ProductService.sort_products(
            db,
            sort_by,
            order
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get("/browse", response_model=ProductListResponse)
def browse_products(
    search: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        products, total = ProductService.browse_products(
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

        return {
            "total": total,
            "page": page,
            "limit": limit,
            "products": products
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
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
        product = ProductService.update(
            db,
            product_id,
            product_data
        )

        # Clear old product cache
        redis_client.delete("products:all")

        return product

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db),current_admin=Depends(require_admin)):
    try:
        ProductService.delete_product(db,product_id)
        redis_client.delete("products:all")
        return{"message":"Product deleted sucessflly"}
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )