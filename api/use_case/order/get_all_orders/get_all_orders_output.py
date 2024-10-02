from dataclasses import dataclass
from typing import List

@dataclass
class GetAllOrdersOutput:
    orders: List[dict]
    result: bool
    exception: Exception = None