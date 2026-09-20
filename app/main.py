from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.database.database import Base,engine
from app.models import user,product,order_items,order,cart,cart_item,category,review
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

@app.get("/")
def root():
    return {"message":"E-comerce api is running"}

@app.get("/db-test")
def db_test(db:Session=Depends(get_db)):
    return {"message":"Database session is working"}
