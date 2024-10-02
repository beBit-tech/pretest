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
    
    '''
    order_lines example:
    [
        {
            "number": "73206538-c3fa-4b4a-8254-2dc13432e573",
            "quantity": 2
        },
        {
            "number": "88c55799-99aa-48e7-9925-70bc6e44b1a8",
            "quantity": 3
        }
    ]
    '''
    
    def __post_init__(self):
        if self.number is None:
            self.number = str(uuid.uuid4())