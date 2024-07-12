import pytest
from unittest.mock import patch

from app.crud_service.user_service import (
    create_user,
    update_user,
    read_users,
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.model.user_model import User, UserUpdate

LOAD_DATA = 'app.crud_service.json_data_helper.JsonDataHelper.load_data'
SAVE_DATA = 'app.crud_service.json_data_helper.JsonDataHelper.save_data'


@pytest.fixture
def test_user_data():
    return [
        {"name": "testuser1", "email": "test1@example.com", "created_at": "2023-11-10 10:00:00",
         "updated_at": "2023-11-12 10:00:00"},
        {"name": "testuser2", "email": "test2@example.com", "created_at": "2023-11-10 11:00:00",
         "updated_at": "2023-11-11 11:00:00"},
    ]


@pytest.fixture
def test_user():
    return User(name="testuser3", email="test3@example.com")


@pytest.fixture
def existing_user():
    return User(name="testuser1", email="test1@example.com")

@pytest.fixture
def updated_user_data():
    return UserUpdate(email="new_email@example.com")


def test_create_user_successfully(test_user_data, test_user, monkeypatch):
    """Тест успешного создания пользователя."""
    with patch(LOAD_DATA) as mock_load_data, patch(SAVE_DATA) as mock_save_data:
        mock_load_data.return_value = test_user_data.copy()

        created_user = create_user(test_user)

        assert created_user.name == test_user.name
        assert created_user.email == test_user.email
        assert created_user.created_at is not None
        mock_save_data.assert_called_once_with(test_user_data + [created_user.model_dump()])


def test_create_user_already_exists(test_user_data, existing_user, monkeypatch):
    """Тестирование create_user при попытке создать существующего пользователя."""
    with patch(LOAD_DATA) as mock_load_data, \
            patch(SAVE_DATA) as mock_save_data:
        mock_load_data.return_value = test_user_data

        with pytest.raises(UserAlreadyExistsException):
            create_user(existing_user)

        mock_save_data.assert_not_called()


def test_update_user_successfully(test_user_data, updated_user_data, monkeypatch):
    """Тестирование функции update_user."""
    with patch(LOAD_DATA) as mock_load_data, \
            patch(SAVE_DATA) as mock_save_data:
        mock_load_data.return_value = test_user_data.copy()

        updated_user = update_user(
            "testuser1", updated_user_data
        )
        assert updated_user.email == "new_email@example.com"
        assert updated_user.updated_at is not None
        mock_save_data.assert_called_once()




def test_update_user_not_found(test_user_data, updated_user_data, monkeypatch):
    """Тестирование update_user, когда пользователь не найден."""
    with patch(LOAD_DATA) as mock_load_data:
        mock_load_data.return_value = test_user_data.copy()

        with pytest.raises(UserNotFoundException):
            update_user("nonexistent_user", updated_user_data)


def test_read_users(test_user_data, monkeypatch):
    """Тестирование функции read_users."""
    with patch(LOAD_DATA) as mock_load_data:
        mock_load_data.return_value = test_user_data
        users = read_users()
        assert len(users) == 2



def test_read_users_empty(monkeypatch):
    """Тестирование read_users, когда нет пользователей."""
    with patch(LOAD_DATA) as mock_load_data:
        mock_load_data.return_value = []
        users = read_users()
        assert users == {"message:": "Пользователей не обнаружено"}
