# src/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings  # Импортируем наши настройки

# Создаем асинхронный "движок" для SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL)

# Создаем фабрику сессий, которая будет создавать новые сессии для каждого запроса
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Функция-зависимость для получения сессии БД
async def get_async_session():
    async with async_session_maker() as session:
        yield session
