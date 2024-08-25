import json
import os
from database.DatabaseInterface import DatabaseInterface

class JSONStorage(DatabaseInterface):
    def __init__(self, configString: str):
        self.file_path = configString

    def connect(self):
        self.file_path = self.file_path

    def disconnect(self):
        pass

    def query(self, query: str, data: list) -> list:
        dbData = self.load()
        
        if query == 'upsert':
            self.upsert(data, dbData)
            self.save(dbData)
        elif query == 'insert':
            self.insert(data, dbData)
            self.save(dbData)

        return data
    def save(self, products: list):
        with open(self.file_path, 'w') as f:
            json.dump([product for product in products], f, indent=4)

    def load(self) -> list:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, 'r') as file:
            data = json.load(file)
            return [(item) for item in data]

    def upsert(self, data: list, dbData: list):
        for item in data:
            if item in dbData:
                self.update([item], dbData)
            else:
                self.insert([item], dbData)

    def insert(self, data: list, dbData: list):
        dbData.extend(data)
    
    def update(self, data: list, dbData:list):
        for item in data:
            if item in dbData:
                index = dbData.index(item)
                dbData[index] = item

