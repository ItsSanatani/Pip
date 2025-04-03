from aiogram import types, Router
from aiogram.filters import Command
from utils.session_store import add_session, list_sessions
from pyrogram import Client
from config import API_ID, API_HASH

router = Router()

async def is_session_valid(session_string: str) -> bool:
    """Check if a given session string is valid."""
    try:
        async with Client("checker", api_id=API_ID, api_hash=API_HASH, session_string=session_string) as client:
            await client.get_me()  # Try fetching user details
        return True
    except Exception:
        return False

@router.message(Command("addsession"))
async def add_session_command(message: types.Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply("❌ <b>Usage:</b> <code>/addsession {session_string}</code>", parse_mode="HTML")
        return

    session_string = args[1].strip()

    if not await is_session_valid(session_string):
        await message.reply("❌ <b>Invalid Session!</b> Please provide a valid session string.", parse_mode="HTML")
        return

    add_session(session_string)
    await message.reply("✅ <b>Session Added Successfully!</b>", parse_mode="HTML")

@router.message(Command("listsessions"))
async def list_sessions_command(message: types.Message):
    sessions = list_sessions()
    if not sessions:
        await message.reply("❌ <b>No sessions added yet.</b>", parse_mode="HTML")
    else:
        await message.reply(f"✅ <b>Active Sessions:</b> <code>{len(sessions)}</code>", parse_mode="HTML")
