from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):    
    text_prompt = State()
    img_prompt = State()
    registered = State()
    event_list_prompt = State()
    initial_state = State()
    update_info = State()
  