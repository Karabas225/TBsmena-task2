import json
import os
from .models import Book

class Storage:
    def __init__(self, filename='data/library.json'):
        self.filename = filename

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return [Book.from_dict(item) for item in data]
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                return []
        return []

    def save(self, books):
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([book.to_dict() for book in books], f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")