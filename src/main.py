# src/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Импортируем сервисы
import services
from database import get_async_session
from schemas import ItemCreate, ItemRead

app = FastAPI(title="My FastAPI Testing App")


@app.post("/items/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(
    item: ItemCreate, db: AsyncSession = Depends(get_async_session)
):
    return await services.create_new_item(item_data=item, db=db)


@app.get("/items/", response_model=List[ItemRead])
async def read_items_endpoint(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_session)
):
    return await services.get_all_items(db=db, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=ItemRead)
async def read_item_endpoint(
    item_id: int, db: AsyncSession = Depends(get_async_session)
):
    db_item = await services.get_item_by_id(item_id=item_id, db=db)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
