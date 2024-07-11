from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class User(BaseModel):
    """Базовая схема для пользователя."""
    name: str
    email: EmailStr
    # Не использую datetime, лишняя обработка сериализации, а также валидации Pydentic при ответе
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя."""
    email: EmailStr
