from pydantic import BaseModel

class CartCreate(BaseModel):
    product_id:int
    quantity:int

class CreateResponse(BaseModel):
    product_id:int
    quantity:int

    class Config:
        from_attributes=True

        
