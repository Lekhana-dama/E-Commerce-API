from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import get_current_user
from app.dependencies.authorization import require_admin
from app.dependencies.database import get_db
from app.schemas.user import UserCreate,UserResponse,UserLogin,TokenResponse
from app.services.user_service import UserService

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse)
def register(user_data:UserCreate,db:Session=Depends(get_db)):
    return UserService.register_user(db,user_data)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return UserService.login_user(
        db,
        form_data.username,
        form_data.password
    )

@router.get("/me",response_model=UserResponse)
def get_profile(current_user=Depends(get_current_user)):
    return current_user

@router.post("/login",response_model=TokenResponse)
def login(user_data:UserLogin,db:Session=Depends(get_db)):
    return UserService.login_user(db,user_data)

@router.get("/admin-test")
def admin_test(current_admin=Depends(require_admin)):
    return{
        "message":"Welcome Admin",
        "user":current_admin.name
    }