# src/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_async_session
from models import Item
from schemas import ItemCreate, ItemRead

app = FastAPI(title="My FastAPI Testing App")


@app.post("/items/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_async_session)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=List[ItemRead])
async def read_items(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    items = result.scalars().all()
    return items


@app.get("/items/{item_id}", response_model=ItemRead)
async def read_item(item_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
