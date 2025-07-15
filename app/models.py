from typing import List, Optional
from pydantic import BaseModel, Field, root_validator, ValidationError

class OrderItem(BaseModel):
    name: str = Field(..., title="Item Name", example="Wireless Mouse")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero", example=1)
    price: float = Field(..., gt=0, description="Price must be greater than zero", example=19.99)

class OrderBase(BaseModel):
    customer: str = Field(..., title="Customer Name", example="Alice Smith")
    items: List[OrderItem] = Field(..., min_items=1, description="Order must include at least one item.")

    @root_validator
    def check_items_not_empty(cls, values):
        items = values.get('items')
        if not items or len(items) == 0:
            raise ValueError('Order must include at least one item.')
        return values

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer: Optional[str] = Field(None, title="Customer Name", example="Bob Jones")
    items: Optional[List[OrderItem]] = Field(None, description="New order items list.")

    @root_validator
    def check_items_if_present(cls, values):
        items = values.get('items')
        if items is not None and len(items) == 0:
            raise ValueError('Order must include at least one item.')
        return values

class Order(OrderBase):
    id: int = Field(..., title="Order ID", example=1001)
