from aiogram.fsm.state import StatesGroup, State

class RouteForm(StatesGroup):
    from_location = State()
    to_location = State()
    travel_date = State()
    luggage = State()
    conditions = State()