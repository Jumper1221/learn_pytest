# src/services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Item
from schemas import ItemCreate


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
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
