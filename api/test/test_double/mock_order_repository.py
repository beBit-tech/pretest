from api.use_case.repository.repository_interface import RepositoryInterface
import uuid

class MockOrderRepository(RepositoryInterface):
    def __init__(self) -> None:
        self.orders = {}
        
    def add(self, data_map: dict) -> None:
        self.orders[data_map["number"]] = data_map

    def get_by_number(self, number: str) -> dict:
        return self.orders.get(number, None)
    