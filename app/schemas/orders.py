from pydantic import BaseModel


class OrderCreate(BaseModel):
    shipping_address: str


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    shipping_address: str
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True