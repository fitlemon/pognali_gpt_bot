from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):    
    text_prompt = State()
    img_prompt = State()
    registered = State()
    event_list_prompt = State()
    another_city_prompt = State()
    change_name = State()
    change_my_city = State()
    change_interests = State()
    initial_state = State()
    update_info = State()
  