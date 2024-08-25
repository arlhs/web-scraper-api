from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self, configString: str):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def query(self, query: str, data: list):
        pass