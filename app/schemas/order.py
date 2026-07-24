from pydantic import BaseModel


class OrderItemResponse(BaseModel):

    product_id:int
    quantity:int
    price:float


    class Config:
        from_attributes=True



class OrderResponse(BaseModel):

    id:int
    total_price:float
    status:str


    class Config:
        from_attributes=True