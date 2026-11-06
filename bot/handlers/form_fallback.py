"""
Ответ на сообщения без текста (стикер, фото, голосовое) во время заполнения анкеты.
Подключается последним, чтобы срабатывать только когда шаг анкеты сообщение не принял.
"""

from aiogram import Router, types, F
from aiogram.filters import StateFilter

router = Router()


@router.message(~StateFilter(None), ~F.text)
async def ask_for_text_answer(message: types.Message):
    await message.answer("✍️ Пожалуйста, отправьте ответ текстом.")
