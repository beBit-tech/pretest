from dataclasses import dataclass

@dataclass
class CreateProductInput:
    name: str
    price: float
    
    def get_name(self) -> str:
        return self.name
    
    def get_price(self) -> float:
        return self.price
    