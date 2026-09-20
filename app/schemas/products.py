from pydantic import BaseModel

class ProductCreate(BaseModel):

    name:str
    description:str |None=None
    price:float
    stock_quantity:int
    category_id:int
    image_url:str|None=None

class ProductResponse(BaseModel):
    id:int
    name:str
    description:str |None
    price:float
    stock_quantity:int
    category_id:int
    image_url:str|None   
    is_active:bool

class Config:
    from_attributes=True


class ProductListResponse(BaseModel):
    total: int
    page: int
    limit: int
    products: list[ProductResponse]