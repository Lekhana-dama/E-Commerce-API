from app.services.cart_service import CartService
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException
from app.dependencies.authorization import get_current_user
from app.dependencies.database  import get_db
from app.schemas.cart import  CreateResponse,CartCreate

router=APIRouter(prefix="/cart",tags=["Cart"])

@router.get("")
def  get_cart(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        cart=CartService.get_cart(db,current_user.id)
        return cart
    except ValueError as e:
        raise HTTPException (
            status_code=404,
            detail=str(e)
        )
@router.post("/items",response_model=CreateResponse)
def add_to_cart(cart_data:CartCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return CartService.add_to_cart(db,current_user.id,cart_data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.put("/items/{item_id}",response_model=CreateResponse)
def update_cart(item_id:int,quantity:int,db:Session=Depends(get_db),cur_user=Depends(get_current_user)):
    try:
        return CartService.update_cart_item(db,cur_user.id,item_id,quantity)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/items/{item_id}")
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return CartService.remove_cart_item(
            db,
            current_user.id,
            item_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )