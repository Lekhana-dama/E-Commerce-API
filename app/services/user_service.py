from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password,verify_password,create_access_token
from app.schemas.user import UserCreate,UserLogin


class UserService:
    @staticmethod
    def register_user(db:Session,user_data:UserCreate):
        existing_user=UserRepository.get_by_email(db,user_data.email)
        if existing_user:
            raise ValueError("Email alreday exits")
        password_hash=hash_password(user_data.password)
        return UserRepository.create(db=db,name=user_data.name,email=user_data.email,password_hash=password_hash)
    @staticmethod
    def login_user(db:Session,email:str,password:str):
        user=UserRepository.get_by_email(db,email)
        if not user:
            raise ValueError("Invalid email or password")
        if not verify_password(password,user.password_hash):
            raise ValueError("Invalid email or passwrod")
        token={
               "sub":str(user.id),
               "role":user.role
               }
        access_token=create_access_token(token)
        return {
            "access_token":access_token,
            "token_type":"bearer"
        }