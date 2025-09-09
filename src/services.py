# src/services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Item
from schemas import ItemCreate
import currency_converter


async def get_item_by_id(item_id: int, db: AsyncSession) -> Item | None:
    """Получает один элемент по его ID."""
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()


async def get_all_items(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Item]:
    """Получает список всех элементов."""
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_new_item(item_data: ItemCreate, db: AsyncSession) -> Item:
    """Создает новый элемент в базе данных."""
    db_item = Item(name=item_data.name, description=item_data.description)
    try:
        # Пытаемся получить данные
        # Обогащаем данными
        rate = await currency_converter.get_usd_to_eur_rate()
        # Предположим, что цена в долларах - это длина имени :)
        price_usd = len(db_item.name)
        db_item.price_eur = round(price_usd * rate, 2)
    except Exception as e:
        # Если внешний сервис вернул ошибку, логируем ее (в реальном проекте)
        # и просто не устанавливаем цену в евро.
        print(f"Could not fetch currency rate: {e}")
        db_item.price_eur = None

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
