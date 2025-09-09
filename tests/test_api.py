# tests/test_items_api.py
import pytest
from httpx import AsyncClient

# Помечаем все тесты в этом файле как асинхронные
pytestmark = pytest.mark.asyncio


async def test_create_item(client: AsyncClient):
    """Тестируем создание элемента."""
    response = await client.post(
        "/items/", json={"name": "Test Item", "description": "This is a test item"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert "id" in data


async def test_read_items(client: AsyncClient):
    """Тестируем чтение списка элементов."""
    # Сначала создадим элемент, чтобы было что читать
    await client.post("/items/", json={"name": "Item 1", "description": "First item"})

    response = await client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Item 1"


async def test_read_specific_item(client: AsyncClient):
    """Тестируем чтение конкретного элемента."""
    # Создаем элемент
    create_response = await client.post(
        "/items/", json={"name": "Specific Item", "description": "Details here"}
    )
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    # Читаем созданный элемент
    read_response = await client.get(f"/items/{item_id}")
    assert read_response.status_code == 200
    data = read_response.json()
    assert data["id"] == item_id
    assert data["name"] == "Specific Item"


async def test_read_non_existent_item(client: AsyncClient):
    """Тестируем чтение несуществующего элемента."""
    response = await client.get("/items/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


# --- Тесты для общих эндпоинтов (из старого файла) ---

# Удаляем тест для '/', так как он не в нашем приложении
# async def test_read_root(client: AsyncClient):
#     """Тестируем корневой эндпоинт."""
#     response = await client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello, World!"}

# Удаляем healthcheck, его тоже нет
# async def test_healthcheck(client: AsyncClient):
#     """Тестируем эндпоинт проверки здоровья."""
#     response = await client.get("/healthcheck")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}
