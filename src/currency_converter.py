# src/currency_converter.py
import asyncio


# В реальном приложении здесь был бы httpx-клиент и запрос к API
async def get_usd_to_eur_rate() -> float:
    """
    Имитирует асинхронный вызов к внешнему API для получения курса валют.
    """
    print("Calling external currency API...")
    # Имитируем задержку сети
    await asyncio.sleep(1)
    print("...external API call finished.")
    return 0.95  # Возвращаем "сегодняшний" курс
