from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.review import ReviewResponse,ReviewCreate
from app.services.review_service import ReviewService
from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.orm import Session

router=APIRouter(prefix="/reviews",tags=["Reviews"])

@router.post("",response_model=ReviewResponse)
def create_review(review:ReviewCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return ReviewService.create_review(db,current_user.id,review)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get("/product/{product_id}",response_model=list[ReviewResponse])
def get_product_review(product_id:int,db:Session=Depends(get_db)):
    try:
        return ReviewService.get_product_reviews(db,product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.put("/{review_id}",response_model=ReviewResponse)
def update_review(id:int,review:ReviewCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return ReviewService.update_review(db=db,id=current_user.id,review_id=id,rating=review.rating,comment=review.comment)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{review_id}")
def delete_review(review_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return ReviewService.delete_review(db=db,user_id=current_user.id,review_id=review_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
