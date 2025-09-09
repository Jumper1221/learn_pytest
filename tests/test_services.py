# tests/test_services.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import services
from schemas import ItemCreate

# Помечаем все тесты в этом файле как асинхронные
pytestmark = pytest.mark.asyncio

async def test_create_new_item(session: AsyncSession):
    """Тестируем функцию создания элемента."""
    item_data = ItemCreate(name="Test Service Item", description="A cool item")
    
    # Вызываем сервисную функцию напрямую
    new_item = await services.create_new_item(item_data=item_data, db=session)

    assert new_item.id is not None
    assert new_item.name == "Test Service Item"
    assert new_item.description == "A cool item"

async def test_get_item_by_id(session: AsyncSession):
    """Тестируем функцию получения элемента по ID."""
    # Сначала создадим элемент, чтобы было что получать
    item_data = ItemCreate(name="Item to get", description="Details")
    new_item = await services.create_new_item(item_data=item_data, db=session)
    
    # Получаем его через сервисную функцию
    retrieved_item = await services.get_item_by_id(item_id=new_item.id, db=session)

    assert retrieved_item is not None
    assert retrieved_item.id == new_item.id
    assert retrieved_item.name == "Item to get"

async def test_get_item_by_id_not_found(session: AsyncSession):
    """Тестируем получение несуществующего элемента."""
    retrieved_item = await services.get_item_by_id(item_id=999, db=session)
    assert retrieved_item is None