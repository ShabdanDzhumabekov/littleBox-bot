"""
Состояния FSM для подачи объявления (AdForm).
"""

from aiogram.fsm.state import StatesGroup, State

class AdForm(StatesGroup):
    type = State()
    description = State()
    from_location = State()
    to_location = State()
    approx_date = State()
    price = State()