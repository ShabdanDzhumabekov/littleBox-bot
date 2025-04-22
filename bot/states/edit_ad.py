from aiogram.fsm.state import State, StatesGroup

class EditAdForm(StatesGroup):
    description = State()
    from_location = State()
    to_location = State()
    approx_date = State()
    price = State()