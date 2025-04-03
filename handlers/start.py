from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply(
        "🚀 <b>Telegram Mass Reporting Bot Running!</b>\n"
        "Use <code>/addsession session_string</code> to add accounts.",
        parse_mode="HTML"
    )
