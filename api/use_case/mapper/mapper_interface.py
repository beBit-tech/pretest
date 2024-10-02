from abc import ABC, abstractmethod

class BaseMapper(ABC):
    
    @staticmethod
    @abstractmethod
    def to_dict(entity) -> dict:
        pass
    
    @staticmethod
    @abstractmethod
    def from_dict(data: dict):
        pass
