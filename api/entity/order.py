from dataclasses import dataclass
from datetime import datetime

@dataclass
class Order:
    order_number: int
    total_price: float
    created_time: datetime