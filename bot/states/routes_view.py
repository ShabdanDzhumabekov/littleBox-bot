from aiogram.fsm.state import StatesGroup, State

class FindRouteForm(StatesGroup):
    from_location = State()
    to_location = State()