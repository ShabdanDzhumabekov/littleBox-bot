"""
Обработчик команды /help: показывает список доступных команд и функций.
"""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Обрабатывает /help и отправляет текст с подсказками.
    """
    await message.answer(
        "🛠 <b>Команды бота:</b>\n"
        "/start — Запустить бота\n"
        "/help — Показать это сообщение\n\n"
        "Также ты можешь использовать кнопки внизу ⬇️"
    )