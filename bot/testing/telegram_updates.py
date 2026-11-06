from datetime import datetime

from aiogram.types import CallbackQuery, Chat, Message, Sticker, Update, User


def text_message_update(user_id: int, text: str) -> Update:
    return Update(update_id=1, message=_message_from(user_id, text=text))


def sticker_message_update(user_id: int) -> Update:
    sticker = Sticker(
        file_id="sticker",
        file_unique_id="sticker",
        type="regular",
        width=512,
        height=512,
        is_animated=False,
        is_video=False,
    )
    return Update(update_id=1, message=_message_from(user_id, sticker=sticker))


def button_press_update(user_id: int, callback_data: str) -> Update:
    callback_query = CallbackQuery(
        id="callback",
        from_user=_user(user_id),
        chat_instance="chat",
        message=_message_from(user_id, text="message with buttons"),
        data=callback_data,
    )
    return Update(update_id=1, callback_query=callback_query)


def _message_from(user_id: int, text: str | None = None, sticker: Sticker | None = None) -> Message:
    return Message(
        message_id=1,
        date=datetime.now(),
        chat=Chat(id=user_id, type="private"),
        from_user=_user(user_id),
        text=text,
        sticker=sticker,
    )


def _user(user_id: int) -> User:
    return User(id=user_id, is_bot=False, first_name="Test")
