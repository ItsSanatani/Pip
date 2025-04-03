from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from utils.report_reasons import REPORT_REASONS
from utils.session_store import list_sessions
from config import API_ID, API_HASH

router = Router()

class ReportState(StatesGroup):
    target = State()
    reason = State()
    count = State()

@router.message(Command("report"))
async def start_report(message: types.Message, state: FSMContext):
    await message.reply("🔍 <b>Enter target username or channel (e.g., @username):</b>", parse_mode="HTML")
    await state.set_state(ReportState.target)

@router.message(ReportState.target)
async def ask_reason(message: types.Message, state: FSMContext):
    await state.update_data(target=message.text.strip())

    keyboard = InlineKeyboardBuilder()
    for key in REPORT_REASONS.keys():
        keyboard.button(text=key.replace("_", " ").title(), callback_data=f"reason:{key}")

    await message.reply("📌 <b>Select a reason:</b>", reply_markup=keyboard.as_markup(), parse_mode="HTML")
    await state.set_state(ReportState.reason)

@router.callback_query(F.data.startswith("reason:"))
async def ask_count(callback: types.CallbackQuery, state: FSMContext):
    reason_key = callback.data.split(":")[1]
    await state.update_data(reason=reason_key)

    await callback.message.edit_text("🔢 <b>Enter the number of reports to send:</b>", parse_mode="HTML")
    await state.set_state(ReportState.count)

@router.message(ReportState.count)
async def process_report(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("❌ <b>Invalid count! Enter a number.</b>", parse_mode="HTML")
        return

    data = await state.get_data()
    target = data['target']
    reason_key = data['reason']
    report_count = int(message.text)

    await state.clear()

    reason = REPORT_REASONS[reason_key]
    total_reports = 0
    failed_count = 0

    for session_string in list_sessions():
        try:
            async with Client(f"session_{hash(session_string)}", api_id=API_ID, api_hash=API_HASH, session_string=session_string) as client:
                peer = await client.resolve_peer(target)

                for _ in range(report_count):
                    await client.invoke(ReportPeer(peer=peer, reason=reason, message="Automated Report"))
                    total_reports += 1

        except Exception as e:
            failed_count += 1
            print(f"⚠️ Failed: {str(e)}")

    await message.reply(
        f"✅ <b>Total Reports Sent:</b> <code>{total_reports}</code> 🚀\n"
        f"❌ <b>Failed Attempts:</b> <code>{failed_count}</code>\n"
        f"📢 <b>Reason Used:</b> <code>{reason_key}</code>",
        parse_mode="HTML"
    )
