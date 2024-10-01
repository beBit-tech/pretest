from typing import List

from api.use_case.repository.repository_interface import RepositoryInterface

class MockOrderRepository(RepositoryInterface):
    def __init__(self) -> None:
        self.orders = []
        
    def add(self, data_map: dict) -> None:
        self.orders.append(data_map)

    def get_by_number(self, number: str) -> dict:
        return next((order for order in self.orders if order.get("number") == number), None)
    
    def get_all(self) -> List[dict]:
        return self.orders
    