from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
import json
import re


import kb
import text


from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import utils
from states import Gen

router = Router()



# Handler for start command at the beginning
@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    
    await msg.answer(
        text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_reg
    )
    data = {
        "user_id": msg.from_user.id,
        "user_name": msg.from_user.username,
        "user_firstname": msg.from_user.full_name,
        "user_surname": "",
        "age": 0,
        "sex": "",
        "about_me": [
            "new user"
        ],
        "topics_history": [
            ""
        ],
        "favorite_films": [
            ""
        ],
        "favorite_books": [
            ""
        ],
        "favorite_shows": [
            ""
        ],
        "favorite_sports": [
            ""
        ],
        "favorite_countries": [
            ""
        ],
        "favorite_cities": [
            ""
        ],
        "favorite_youtube_channels": [
            ""
        ],
        "user_city": "unknown",
        "user_interests": [
            ""
        ],
        "last_question": ""
    }
    await utils.add_new_user_data(data, msg.from_user.id)
    await state.set_state(Gen.initial_state)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    await msg.answer("Выходим в главное меню...", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Gen.initial_state)
    await msg.answer(text.menu, reply_markup=kb.menu_reg)


# Handler for catch "Where to go?!" button pushing
@router.callback_query(F.data == "my_city_events")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.event_list_prompt)
    await clbck.message.answer(text.gen_text)
    #await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    user_data = await utils.get_user_data(clbck.message.chat.id)
    res = await utils.generate_events_list(user_data)
    if not res:
        return await clbck.message.answer(text.gen_error, reply_markup=kb.exit_kb)
    
    await clbck.message.answer(
        res[0] + text.text_watermark, disable_web_page_preview=True, reply_markup=kb.exit_kb
    )
    await state.set_state(Gen.text_prompt)

# Handler for "Change my info" button
@router.callback_query(F.data == "my_info")
async def get_my_info(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.update_info) 
    user_data = await utils.get_user_data(clbck.message.chat.id)
    await clbck.message.answer(text.gen_text)
    question = 'Я рад снова вернуться на интервью!'
    await utils.add_last_question(question, clbck.message.chat.id)    
    #res = await utils.update_info_prompt("Расскажи что ты знаешь обо мне. А потом продолжай задавать вопросы", user_data)
    res = await utils.prompt_to_dude("Я тоже, Продолжай задавать вопросы, чтобы побольше узнать обо мне", user_data)
    if not res:
        return await clbck.message.answer(text.gen_error)
    try:
        # json_data = json.loads(res[0].replace("'",'"').split("_masktosplit_")[1])        
        # await utils.update_user_data(json_data, clbck.message.chat.id)
        question = res[0]
        await utils.add_last_question(question, clbck.message.chat.id)
        await clbck.message.answer(res[0] + text.text_watermark, disable_web_page_preview=True)
        
    except:
        await clbck.message.answer(res[0] + text.text_watermark, disable_web_page_preview=True)
       
 ## Handler for messages in "Update info" State  
@router.message(Gen.update_info)
async def change_name(msg: Message, state: FSMContext):
    await state.set_state(Gen.update_info) 
    user_data = await utils.get_user_data(msg.from_user.id)
    await msg.answer(text.gen_text)
    #res = await utils.update_info_prompt(msg.text, user_data)
    res = await utils.prompt_to_dude(msg.text, user_data)
    
    # if not res:
    #     return await msg.edit_text(text.gen_error)
           
    # pattern = re.compile(r"({[^}]*})", re.DOTALL)
    # match = pattern.search(res[0])
    # if match:
    #     print("НАШЕЛСЯ!!")
    #     dictionary_text = match.group(1)
    #     question = res[0].replace(dictionary_text, "")
    #     #print(dictionary_text)
    #     await utils.add_last_question(question, msg.from_user.id)
    #     json_data = json.loads(dictionary_text.replace("'",'"'))
    #     await utils.update_user_data(json_data, msg.from_user.id)
    # else:
    #      print("НЕ НАШЕЛСЯ!!")        
    # await utils.update_user_data(json_data, msg.from_user.id)
    await msg.answer(res[0] + text.text_watermark, disable_web_page_preview=True)
    dict_res = await utils.prompt_to_dict_changer(msg.text, user_data)
    json_data = json.loads(dict_res[0].replace("'",'"'))
    print(json_data)
    await utils.update_user_data(json_data, msg.from_user.id)
    await msg.answer(dict_res[0] + text.text_watermark, disable_web_page_preview=True)
    if res:
        await utils.add_last_question(res[0], msg.from_user.id)   
    
        
        
                
# ## Handler for "Change my info" button
# @router.callback_query(F.data == "my_info")
# async def get_my_info(clbck: CallbackQuery, state: FSMContext):    
#     user_data = await utils.get_user_data(clbck.message.chat.id)
#     if user_data:   
#         await clbck.message.answer(text.my_info.format(name=user_data['user_fullname'], city=user_data['city'], interests=user_data['interest']))
#         await clbck.message.answer(text.change_info, reply_markup=kb.change_info_kb)        
#     else:
#         await clbck.message.edit_text("Я не знаю ничего о тебе(")


## Handler for "Change my info confirm" button    
@router.callback_query(F.data == "change_my_info")
@flags.chat_action("typing")
async def change_my_info(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.change_name)
    await state.set_state(Gen.change_name)


## Handler for messages in "Change name" State  
@router.message(Gen.change_name)
async def change_name(msg: Message, state: FSMContext):
    user_data = await utils.get_user_data(msg.from_user.id)
    if user_data:
        user_data['user_fullname'] = msg.text
        await utils.update_user_data(user_data, msg.from_user.id)
        await msg.answer(text.change_my_city.format(name=msg.text), reply_markup=kb.change_my_city_kb)
        await state.set_state(Gen.change_my_city) 
 
 

## Handler for messages in "Change my city" State         
@router.message(Gen.change_my_city)
async def change_my_city(msg: Message, state: FSMContext):
    user_data = await utils.get_user_data(msg.from_user.id)
    if user_data:
        user_data['city'] = msg.text
        await utils.update_user_data(user_data, msg.from_user.id)
        await msg.answer(text.change_interests.format(name=user_data['user_fullname'], city=msg.text))
        await state.set_state(Gen.change_interests) 


## Handler for messages in "Change my interests" State 
@router.message(Gen.change_interests)
async def change_my_city(msg: Message, state: FSMContext):
    user_data = await utils.get_user_data(msg.from_user.id)
    if user_data:
        user_data['interest'] = re.split(' |\; |, |\*|\n| и ', msg.text)
        await utils.update_user_data(user_data, msg.from_user.id)
        await msg.answer(text.change_info_done.format(name=user_data['user_fullname'], city=user_data['city'], interests=user_data['interest']))
        await state.set_state(Gen.initial_state) 

## Handler for messages in "Text Prompt" State 
@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    user_data = await utils.get_user_data(msg.from_user.id)
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(msg.text, user_data)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    try:
        json_data = json.loads(res[0].replace("'",'"'))
        await utils.update_user_data(json_data, msg.from_user.id)
    except:
        await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)
        


@router.callback_query(F.data == "another_city")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.another_city_prompt)
    await clbck.message.edit_text(text.another_city)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.another_city)


@router.callback_query(F.data == "another_city_confirm")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.another_city_prompt)
    await clbck.message.edit_text(text.another_city)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.another_city)


# @router.callback_query(F.data == "generate_image")
# async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
#     await state.set_state(Gen.img_prompt)
#     await clbck.message.edit_text(text.gen_image)
#     await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


# @router.message(Gen.img_prompt)
# @flags.chat_action("upload_photo")
# async def generate_image(msg: Message, state: FSMContext):
#     prompt = msg.text
#     mesg = await msg.answer(text.gen_wait)
#     img_res = await utils.generate_image(prompt)
#     if len(img_res) == 0:
#         return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
#     await mesg.delete()
#     await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)