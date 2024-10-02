from dataclasses import dataclass

@dataclass
class CreateProductInput:
    name: str
    price: float