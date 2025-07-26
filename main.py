import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers.base import router as base_router
from handlers.assessment import router as assessment_router
from handlers.imt import router as imt_router
from handlers.program import router as program_router

from database.queries import init_db

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # init_db();
    
    dp.include_router(base_router)
    dp.include_router(assessment_router)
    dp.include_router(imt_router)
    dp.include_router(program_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())