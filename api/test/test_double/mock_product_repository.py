from api.use_case.repository.repository_interface import RepositoryInterface
import uuid

class MockProductRepository(RepositoryInterface):
    def __init__(self) -> None:
        self.products = {}
        
    def add(self, data_map: dict) -> None:
        self.products[data_map[id]] = data_map
        
    def get_by_id(self, id: str) -> dict:
        return self.products[id]
    