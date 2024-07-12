import json
from typing import Optional, List


class JsonDataHelper:
    """Класс для работы с хранилищем данных в формате JSON."""

    def __init__(self, data_file: str):
        self.data_file = data_file

    def user_exists(self, user_name: Optional[str] = None, user_email: Optional[str] = None) -> bool:
        """Проверяет, существует ли пользователь с заданным именем или email."""
        users = self.load_data()
        for user_data in users:
            if (user_name is not None and user_data.get("name") == user_name) or \
                    (user_email is not None and user_data.get("email") == user_email):
                return True
        return False

    def load_data(self) -> List[dict]:
        """Загружает данные из файла."""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self, data: list):
        """Сохраняет данные в файл."""
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)
