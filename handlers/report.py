from aiogram import types, Router
from aiogram.filters import Command
from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from utils.report_reasons import REPORT_REASONS
from utils.session_store import list_sessions
from config import API_ID, API_HASH

router = Router()

@router.message(Command("report"))
async def report_user(message: types.Message):
    args = message.text.split(" ")

    if len(args) < 4:
        await message.reply(
            "❌ *Usage:* `/report @username reason count`\n\n"
            "📝 *Available Reasons:*\n"
            "`spam, violence, child_abuse, pornography, copyright, fake, drugs, personal_data, other`"
        )
        return

    target_user = args[1].strip()
    reason_key = args[2].strip().lower()
    report_count = int(args[3]) if args[3].isdigit() else 1  

    if reason_key not in REPORT_REASONS:
        await message.reply("❌ *Invalid reason!* Use one of these:\n`" + "`, `".join(REPORT_REASONS.keys()) + "`")
        return

    reason = REPORT_REASONS[reason_key]
    total_reports = 0
    failed_count = 0

    for session_string in list_sessions():
        try:
            async with Client("session", api_id=API_ID, api_hash=API_HASH, session_string=session_string) as client:
                user = await client.resolve_peer(target_user)

                for _ in range(report_count):
                    await client.invoke(ReportPeer(peer=user, reason=reason, message="Automated Report"))
                    total_reports += 1

        except Exception as e:
            failed_count += 1
            print(f"⚠️ Failed: {str(e)}")

    reason_key = reason_key.replace("_", "\\_")  

    await message.reply(
        f"✅ *Total Reports Sent:* `{total_reports}` 🚀\n"
        f"❌ *Failed Attempts:* `{failed_count}`\n"
        f"📢 *Reason Used:* `{reason_key}`"
    )
