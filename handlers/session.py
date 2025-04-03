from aiogram import types, Router
from aiogram.filters import Command
from utils.session_store import add_session, list_sessions

router = Router()

@router.message(Command("addsession"))
async def add_session_command(message: types.Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply("❌ <b>Usage:</b> <code>/addsession {session_string}</code>", parse_mode="HTML")
        return

    session_string = args[1].strip()
    add_session(session_string)
    await message.reply("✅ <b>Session Added Successfully!</b>", parse_mode="HTML")

@router.message(Command("listsessions"))
async def list_sessions_command(message: types.Message):
    sessions = list_sessions()
    if not sessions:
        await message.reply("❌ <b>No sessions added yet.</b>", parse_mode="HTML")
    else:
        await message.reply(f"✅ <b>Active Sessions:</b> <code>{len(sessions)}</code>", parse_mode="HTML")
