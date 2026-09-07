from fastapi import FastAPI


app=FastAPI(
    title="E-Commerce_API",
    description="Production-style E-Commerce Backend API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message":"E-comerce api is running"}