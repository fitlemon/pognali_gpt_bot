from aiogram.fsm.state import StatesGroup, State


class Gen(StatesGroup):
    initial_state = State()
    where_to_go = State()
    update_info = State()
    events = State()
    events_by_genre = State()
    events_by_desc = State()
    events_by_desc_and_user_data = State()
    events_by_location = State()
    events_popular = State()
    events_recomend = State()
    venues = State()
    venues_by_genre = State()
    venues_by_location = State()
    venues_popular = State()
    venues_recomend = State()
