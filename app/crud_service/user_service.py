import os
from datetime import datetime
from typing import List, Union

from app.model.user_model import User, UserUpdate
from app.crud_service.json_data_helper import JsonDataHelper

DATA_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "users.json")
)
data_helper = JsonDataHelper(DATA_FILE)


class UserNotFoundException(Exception):
    """Исключение, вызываемое, когда пользователь не найден."""
    pass


class UserAlreadyExistsException(Exception):
    """Исключение, вызываемое, когда пользователь с таким именем или email уже существует."""
    pass


def create_user(user: User):
    """
    Создает нового пользователя.
    Возвращает объект нового пользователя
    """
    users = data_helper.load_data()

    if any(user_data.get("name") == user.name for user_data in users):
        raise UserAlreadyExistsException("Пользователь с таким именем уже существует")
    if any(user_data.get("email") == user.email for user_data in users):
        raise UserAlreadyExistsException("Пользователь с таким email уже существует")

    user_data = user.model_dump()
    user_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users.append(user_data)
    data_helper.save_data(users)
    return User(**user_data)


def update_user(user_name: str, user_update: UserUpdate):
    """
    Обновляет данные пользователя.
    Возвращает объект нового пользователя
    """
    users = data_helper.load_data()

    for user_data in users:
        if user_data.get("name") == user_name:
            if user_update.email and data_helper.user_exists(user_email=user_update.email):
                raise UserAlreadyExistsException("Пользователь с таким email уже существует")
            user_data["email"] = user_update.email or user_data.get("email")
            user_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_helper.save_data(users)
            return User(**user_data)
    raise UserNotFoundException("Пользователь не найден")


def read_users() -> Union[List[User], dict]:
    """
    Возвращает данные пользователей из файла.
    Возвращает сообщение, если пользователей не обнаружено.
    """
    users = [User(**user_data) for user_data in data_helper.load_data()]
    if not users:
        return {"message:": "Пользователей не обнаружено"}  # Возвращаем строку, если список пуст
    return users
