from api.use_case.repository.repository_interface import RepositoryInterface
import uuid

class MockProductRepository(RepositoryInterface):
    def __init__(self) -> None:
        self.products = {}
        
    def add(self, data_map: dict) -> None:
        self.products[data_map["number"]] = data_map
        
    def get_by_number(self, number: str) -> dict:
        return self.products.get(number, None)
    
    def check_products_exist(self, product_numbers: list) -> bool:
        return all(product_number in self.products for product_number in product_numbers)