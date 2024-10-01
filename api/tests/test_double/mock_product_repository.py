from typing import List
from api.use_case.repository.repository_interface import RepositoryInterface

class MockProductRepository(RepositoryInterface):
    def __init__(self) -> None:
        self.products = []
        
    def add(self, data_map: dict) -> None:
        self.products.append(data_map)
        
    def get_by_number(self, number: str) -> dict:
        return next((product for product in self.products if product.get("number") == number))
    
    def check_products_exist(self, product_numbers: list) -> set:
        existing_numbers = set(product_numbers) & {product["number"] for product in self.products}
        missing_numbers = set(product_numbers) - existing_numbers
        
        return missing_numbers
    
    def get_all(self) -> List[dict]:
        return self.products