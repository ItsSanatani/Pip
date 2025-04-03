import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, session, report, linkreport

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="MarkdownV2")
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(session.router)
dp.include_router(report.router)
dp.include_router(linkreport.router)

async def main():
    print("🚀 Telegram Mass Reporting Bot Started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
