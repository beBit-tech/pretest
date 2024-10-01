from typing import List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImportOrderInput:
    total_price: float 
    created_time: datetime
    order_lines: List[dict]