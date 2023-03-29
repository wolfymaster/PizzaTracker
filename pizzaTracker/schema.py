from pydantic import BaseModel
from typing import ForwardRef


class OrderItemBase(BaseModel):
    name: str
    price: float
    quantity: int


class OrderBase(BaseModel):
    total: float
    items: list[OrderItemBase] = []


class OrderCreate(OrderBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True
        fields = {
            'id': {'exclude': True},
        }


class Order(OrderBase):
    id: int
    status: str
    items: list[OrderItem] = []

    class Config:
        orm_mode = True


OrderItem.update_forward_refs()
