from aiogram import types, Router
from aiogram.filters import Command
from utils.session_store import add_session, list_sessions

router = Router()

@router.message(Command("addsession"))
async def add_session_command(message: types.Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply("❌ *Usage:* `/addsession {session_string}`")
        return

    session_string = args[1].strip()
    add_session(session_string)
    await message.reply("✅ *Session Added Successfully!*")

@router.message(Command("listsessions"))
async def list_sessions_command(message: types.Message):
    sessions = list_sessions()
    if not sessions:
        await message.reply("❌ *No sessions added yet.*")
    else:
        await message.reply(f"✅ *Active Sessions:* `{len(sessions)}`")
