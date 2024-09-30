from dataclasses import dataclass

@dataclass
class CreateProductOutput:
    product_number: str
    result: bool
    exception: Exception = None