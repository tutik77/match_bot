import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from settings import settings
from database import init_db
from service import gpt_service
from register import router as register_router
from search import router as search_router


bot = Bot(token=settings.bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(register_router)
dp.include_router(search_router)

async def main():
    await init_db()
    await gpt_service.initialize_assistant()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
