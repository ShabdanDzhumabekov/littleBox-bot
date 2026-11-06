from collections.abc import AsyncGenerator, Mapping
from datetime import datetime
from typing import Any

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.exceptions import TelegramForbiddenError
from aiogram.methods import AnswerCallbackQuery, SendMessage, TelegramMethod
from aiogram.types import Chat, Message


class FakeTelegram(BaseSession):
    """Сессия Bot API, которая записывает исходящие вызовы вместо отправки."""

    def __init__(self, blocked_chat_ids: frozenset[int] = frozenset()) -> None:
        super().__init__()
        self.sent_messages: list[SendMessage] = []
        self.callback_answers: list[AnswerCallbackQuery] = []
        self._blocked_chat_ids = blocked_chat_ids

    async def make_request(self, bot: Bot, method: TelegramMethod[Any], timeout: int | None = None) -> Any:
        if isinstance(method, SendMessage):
            return self._send_message(method)
        if isinstance(method, AnswerCallbackQuery):
            self.callback_answers.append(method)
        return True

    def texts_sent_to(self, chat_id: int) -> list[str]:
        return [message.text for message in self.sent_messages if message.chat_id == chat_id]

    def buttons_of_last_message_to(self, chat_id: int) -> list[str]:
        last_message = [message for message in self.sent_messages if message.chat_id == chat_id][-1]
        if last_message.reply_markup is None:
            return []
        return [button.callback_data for row in last_message.reply_markup.inline_keyboard for button in row]

    async def stream_content(
        self,
        url: str,
        headers: Mapping[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        yield b""

    async def close(self) -> None:
        pass

    def _send_message(self, method: SendMessage) -> Message:
        if method.chat_id in self._blocked_chat_ids:
            raise TelegramForbiddenError(method=method, message="Forbidden: bot was blocked by the user")
        self.sent_messages.append(method)
        return Message(
            message_id=len(self.sent_messages),
            date=datetime.now(),
            chat=Chat(id=method.chat_id, type="private"),
            text=method.text,
        )
