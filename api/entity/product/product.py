from dataclasses import dataclass
import uuid

@dataclass
class Product:
    name: str
    price: float
    number: str = None
    
    def __post_init__(self):
        if self.number is None:
            self.number = str(uuid.uuid4())