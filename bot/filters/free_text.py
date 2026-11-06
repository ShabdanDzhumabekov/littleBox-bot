from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.keyboards.admin_menu import admin_keyboard
from bot.keyboards.menu import main_menu

_KEYBOARD_BUTTON_TEXTS = frozenset(
    button.text
    for keyboard in (main_menu(is_admin=True), admin_keyboard)
    for row in keyboard.keyboard
    for button in row
)


class IsFreeText(BaseFilter):
    """
    Пропускает только текст, набранный пользователем. Нажатие кнопки меню посреди
    анкеты должно запускать свой сценарий, а не сохраняться как ответ.
    """

    async def __call__(self, message: Message) -> bool:
        return message.text is not None and message.text not in _KEYBOARD_BUTTON_TEXTS
