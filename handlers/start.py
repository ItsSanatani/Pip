from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("🚀 *Telegram Mass Reporting Bot Running!*\nUse `/addsession {session_string}` to add accounts.")
