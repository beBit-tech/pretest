from abc import ABC, abstractmethod

class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, data_map: dict) -> int:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> dict:
        pass