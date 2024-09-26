from abc import ABC, abstractmethod
from entity.product.product import Product

class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, product: Product) -> dict:
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> dict:
        pass

    @abstractmethod
    def update(self, id: int, data_map: dict) -> dict:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass