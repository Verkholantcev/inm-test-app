import os
import json
from typing import Optional

DATA_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "users.json")
)


def user_exists(user_name: Optional[str] = None, user_email: Optional[str] = None) -> bool:
    """Проверяет, существует ли пользователь с заданным именем или email."""
    users = load_users()
    for user_data in users:
        if (user_name is not None and user_data.get("name") == user_name) or \
                (user_email is not None and user_data.get("email") == user_email):
            return True
    return False


def load_users():
    """Загружает данные пользователей из файла."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_users(users: list):
    """Сохраняет данные пользователей в файл."""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)
