from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    price: float
    
    def get_id(self) -> str:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_price(self) -> float:
        return self.price