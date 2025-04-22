from datetime import datetime, timedelta, date
from typing import Union, Tuple

def validate_date_input(date_str: str, max_days: Union[int, None] = None) -> Tuple[bool, Union[str, date]]:
    """
    Проверяет корректность даты в формате ДД.ММ.ГГГГ и,
    при необходимости, ограничение на максимальное количество дней вперёд.

    :param date_str: строка с датой от пользователя
    :param max_days: если задано — ограничение по числу дней вперёд от текущей даты
    :return: (True, date) если всё ок, иначе (False, сообщение об ошибке)
    """
    try:
        parsed_date = datetime.strptime(date_str.strip(), "%d.%m.%Y").date()
    except ValueError:
        return False, "❗ Неверный формат. Введите дату в формате <code>ДД.ММ.ГГГГ</code>."

    today = datetime.now().date()
    if parsed_date < today:
        return False, "❗ Дата не может быть в прошлом."

    if max_days is not None:
        max_date = today + timedelta(days=max_days)
        if parsed_date > max_date:
            return False, f"❗ Максимальная дата — {max_date.strftime('%d.%m.%Y')}."

    return True, parsed_date