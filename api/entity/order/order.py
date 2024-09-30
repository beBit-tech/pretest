from typing import List
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Order:
    total_price: float
    created_time: datetime
    order_lines: List[dict]
    number: str = None
    
    def __post_init__(self):
        if self.number is None:
            self.number = str(uuid.uuid4())