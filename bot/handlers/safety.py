from aiogram import Router, types, F
from aiogram.filters import Command
from bot.filters.is_admin import IsAdmin
from bot.keyboards.menu import main_menu

router = Router()

SAFETY_TEXT = (
    "🛡 <b>Правила безопасности</b>\n\n"
    "1. Никогда не переводите деньги заранее.\n"
    "2. Проверяйте личность отправителя/путешественника.\n"
    "3. Встречайтесь лично, если возможно.\n"
    "4. Не передавайте важные документы или ценные вещи без проверки.\n"
    "5. littleBox — только платформа для связи, не гарантирует надёжность пользователей.\n\n"
)

@router.message(Command("rules"))
@router.message(F.text == "📌 Безопасность")
async def show_safety(message: types.Message):
    await message.answer(SAFETY_TEXT, parse_mode="HTML")