from dataclasses import dataclass
from typing import List

@dataclass
class GetAllProductsOutput:
    products: List[dict]
    result: bool
    exception: Exception = None