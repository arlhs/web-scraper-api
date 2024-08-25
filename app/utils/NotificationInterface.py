from abc import ABC, abstractmethod

class NotificationInterface(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass