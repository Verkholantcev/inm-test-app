import os
import pytest
import tempfile
from fastapi.testclient import TestClient

from app.main import app
from app.crud_service import user_service as us


@pytest.fixture(autouse=True)
def setup_teardown():
    """Используем временный файл для тестов."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("[]")
        temp_file.flush()
        # Изменяем DATA_FILE на время теста
        original_data_file = us.DATA_FILE  # Сохраняем оригинальный путь
        us.DATA_FILE = temp_file.name
    yield
    # Восстанавливаем оригинальный путь к файлу данных
    us.DATA_FILE = original_data_file
    os.remove(temp_file.name)


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_create_user(client):
    # Тест успешного создания пользователя
    response = client.post("/users/", json={"name": "testuser1", "email": "test1@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "testuser1"
    assert response.json()["email"] == "test1@example.com"

    # Тест создания пользователя с существующим именем
    response = client.post("/users/", json={"name": "testuser1", "email": "test2@example.com"})
    assert response.status_code == 400

    # Тест создания пользователя с существующим email
    response = client.post("/users/", json={"name": "testuser2", "email": "test1@example.com"})
    assert response.status_code == 400


def test_update_user(client):
    # Создаем пользователя для тестов обновления
    client.post("/users/", json={"name": "testuser1", "email": "test1@example.com"})
    client.post("/users/", json={"name": "testuser2", "email": "test2@example.com"})

    # Тест успешного обновления email
    response = client.put("/users/testuser1/", json={"email": "new_email@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "new_email@example.com"

    # Тест обновления на существующий email другого пользователя
    response = client.put("/users/testuser1/", json={"email": "test2@example.com"})
    assert response.status_code == 400

    # Тест обновления несуществующего пользователя
    response = client.put("/users/nonexistent_user/", json={"email": "test@example.com"})
    assert response.status_code == 404


def test_get_users(client):
    client.post("/users/", json={"name": "testuser1", "email": "test1@example.com"})
    client.post("/users/", json={"name": "testuser2", "email": "test2@example.com"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2
