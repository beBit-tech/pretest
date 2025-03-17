from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemData(BaseModel):
    product_number: str
    quantity: int


class OrderData(BaseModel):
    order_number: str
    total_price: float
    customer_name: str
    products: List[OrderItemData] = Field(min_items=1)


class ProductData(BaseModel):
    product_number: str
    product_name: str
    price: float
    stock_quantity: int
    description: Optional[str] = ""


class ProductDeleteData(BaseModel):
    product_number: str


class Status(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
