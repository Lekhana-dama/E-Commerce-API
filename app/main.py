from fastapi import FastAPI, Depends,Request
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.database.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
from app.models import user,product,order_items,order,cart,cart_item,category,review
from config import FRONTEND_URL
from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.product_router import router as product_router
from app.routers.cart import router as cart_router
from app.routers.order import router as order_router
from app.routers.review import router as review_router
from app.routers.upload import router as upload_router
from app.routers.redis_router import router as redis_router

Base.metadata.create_all(bind=engine)


app=FastAPI(
    title="E-Commerce_API",
    description="Production-style E-Commerce Backend API",
    version="1.0.0",
)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(review_router)
app.include_router(upload_router)
app.include_router(redis_router)

@app.middleware("http")
async def add_securty_header(request:Request,call_next):
    response=await call_next(request)

    response.headers["X-Content-Type-Options"]="nosniff"
    response.headers["X-Frame-Options"]="DENY"
    response.headers["Referrer-Policy"]="no-referrer"

    return response

app.add_middleware(CORSMiddleware,allow_origins=[FRONTEND_URL],
                   allow_credentials=True,
                   allow_methods=["GET","POST","PUT","DELETE"],
                   allow_headers=["Authorization","Content-Type"])

@app.get("/")
def root():
    return {
        "message": "E-Commerce API is running"
    }