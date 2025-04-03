from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply("🚀 Telegram Mass Reporting Bot Running\\!\nUse /addsession {session_string} to add accounts.")
