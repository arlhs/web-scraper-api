from utils.NotificationInterface import NotificationInterface

class ConsoleNotification(NotificationInterface):
    def notify(message: str):
        print(f"{message}")