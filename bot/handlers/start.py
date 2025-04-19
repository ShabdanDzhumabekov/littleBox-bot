"""
Обработка команды /start. Показывает приветствие и основную информацию.
"""

from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.menu import main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я бот, который поможет передавать посылки через путешественников.\n\n"
        "Нажми /help для списка команд.",
        reply_markup=main_menu()
    )