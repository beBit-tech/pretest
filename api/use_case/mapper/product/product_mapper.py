from api.use_case.mapper.mapper_interface import BaseMapper
from api.entity.product.product import Product

class ProductMapper(BaseMapper):
    
    @staticmethod
    def to_dict(entity: Product) -> dict:
        return {
            "number": entity.number,
            "name": entity.name,
            "price": entity.price
        }
    
    @staticmethod
    def from_dict(data_map: dict):
        return Product(number = data_map["number"], name = data_map["name"], price = data_map["price"])