from api.use_case.repository.repository_interface import RepositoryInterface
import uuid

class MockOrderRepository(RepositoryInterface):
    def __init__(self) -> None:
        self.orders = {}
        
    def add(self, data_map: dict) -> str:
        id = str(uuid.uuid4())
        self.orders[data_map[id]] = data_map
        return id
    