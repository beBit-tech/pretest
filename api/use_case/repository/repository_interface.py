from abc import ABC, abstractmethod

class RepositoryInterface(ABC):
    @abstractmethod
    def add(self, data_map: dict):
        pass

    @abstractmethod
    def get_all(self, number: str) -> dict:
        pass