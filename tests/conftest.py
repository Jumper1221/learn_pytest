# tests/conftest.py
import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from database import get_async_session
from models import Base
from main import app as fastapi_app
from config import settings

# Используем URL тестовой базы данных и NullPool, чтобы избежать проблем с соединениями
test_engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
test_async_session_maker = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


# Эта фикстура создает и удаляет таблицы для всей тестовой сессии
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Фикстура, которая создает новую сессию для КАЖДОГО теста
@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    # Начинаем транзакцию
    async with test_engine.connect() as connection:
        await connection.begin()
        async with test_async_session_maker(bind=connection) as session:
            yield session
        # Откатываем транзакцию после завершения теста
        await connection.rollback()


# Фикстура, которая предоставляет наше приложение
@pytest.fixture(scope="function")
def app(session: AsyncSession) -> FastAPI:
    # Для каждого теста мы подменяем зависимость get_async_session
    # на функцию, которая возвращает нашу тестовую сессию
    def override_get_session():
        yield session

    fastapi_app.dependency_overrides[get_async_session] = override_get_session
    return fastapi_app


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Фикстура клиента чтобы для каждого теста
# создавался новый клиент с новой подменой зависимости
@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
