# tests/test_services.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import services
from schemas import ItemCreate
from pytest_mock import MockerFixture

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


async def test_create_new_item_with_mocked_currency(
    session: AsyncSession, mocker: MockerFixture
):
    """
    Тестируем создание элемента, мокируя вызов к внешнему API.
    """
    # 1. Настраиваем мок
    # Мы "патчим" функцию get_usd_to_eur_rate в том месте, где она ИСПОЛЬЗУЕТСЯ (в модуле services)
    # и указываем, что она должна возвращать фиксированное значение 0.9
    mock_get_rate = mocker.patch(
        "services.currency_converter.get_usd_to_eur_rate", return_value=0.9
    )

    item_data = ItemCreate(name="My Item", description="A valuable item")

    # 2. Вызываем наш сервис
    new_item = await services.create_new_item(item_data=item_data, db=session)

    # 3. Проверяем результат
    # Длина имени "My Item" = 7. 7 * 0.9 = 6.3
    assert new_item.price_eur == 6.30
    assert new_item.name == "My Item"

    # 4. Проверяем, что мок был вызван
    mock_get_rate.assert_called_once()


async def test_create_item_when_currency_api_fails(
    session: AsyncSession, 
    mocker: MockerFixture
):
    """
    Тестируем, что цена не будет установлена, если API валют вернет ошибку.
    """
    # Настраиваем мок, чтобы он вызывал исключение при вызове
    mocker.patch(
        "services.currency_converter.get_usd_to_eur_rate",
        side_effect=Exception("API is down!")
    )
    
    item_data = ItemCreate(name="Another Item", description="Will it work?")
    
    # Мы ожидаем, что наш сервис "проглотит" ошибку и просто не запишет цену
    # В более сложной системе здесь мог бы быть вызов pytest.raises
    new_item = await services.create_new_item(item_data=item_data, db=session)
    
    # Проверяем, что цена не установилась
    assert new_item.price_eur is None
    assert new_item.name == "Another Item"