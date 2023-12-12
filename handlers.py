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


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer(
        text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_reg
    )
    data = {
        "user_id": msg.from_user.id,
        "user_name": msg.from_user.username,
        "user_fullname": msg.from_user.full_name,
        "session": msg.chat.id,
        "city": "unknown",
        "interest": [],
    }
    json_data = json.load(open("db.json"))
    if not [user for user in json_data if user['user_id'] == msg.from_user.id]:
        json_data.append(data)
        with open("db.json", "w") as outfile:
            json.dump(json_data, outfile)

    await state.set_state(Gen.initial_state) 
# @router.message(Command("start"))
# async def start_handler(msg: Message):
#     await msg.answer(
#         text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_intro
#     )


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    await msg.answer("Выходим в главное меню...", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Gen.initial_state)
    await msg.answer(text.menu, reply_markup=kb.menu_reg)


@router.callback_query(F.data == "my_city_events")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.event_list_prompt)
    await clbck.message.answer(text.gen_text)
    #await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    json_data = json.load(open("db.json"))
    user_data = [data for data in json_data if data['user_id'] == clbck.message.chat.id]
    res = await utils.generate_events_list(user_data)
    if not res:
        return await clbck.message.answer(text.gen_error, reply_markup=kb.exit_kb)
    
    await clbck.message.answer(
        res[0] + text.text_watermark, disable_web_page_preview=True, reply_markup=kb.exit_kb
    )
    await state.set_state(Gen.text_prompt)


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


@router.callback_query(F.data == "my_info")
async def get_my_info(clbck: CallbackQuery, state: FSMContext):
    
    json_data = json.load(open("db.json"))
    user_data = [data for data in json_data if data['user_id'] == clbck.message.chat.id]
    if user_data:
        user_data = user_data[0]    
        await clbck.message.answer(text.my_info.format(name=user_data['user_fullname'], city=user_data['city'], interests=user_data['interest']))
        await clbck.message.answer(text.change_info, reply_markup=kb.change_info_kb)        
    else:
        await clbck.message.edit_text("Я не знаю ничего о тебе(")
    
@router.callback_query(F.data == "change_my_info")
async def change_my_info(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.change_name)
    await state.set_state(Gen.change_name)

@router.message(Gen.change_name)
async def change_name(msg: Message, state: FSMContext):
    json_data = json.load(open("db.json", encoding='utf8'))
    user_data = [i for i, data in enumerate(json_data) if data['user_id'] == msg.from_user.id]
    if user_data:
        user_data = json_data[user_data[0]]
        user_data['user_fullname'] = msg.text
        with open("db.json", "w") as outfile:
            json.dump(json_data, outfile, ensure_ascii=False)
        await msg.answer(text.change_my_city.format(name=msg.text), reply_markup=kb.change_my_city_kb)
        await state.set_state(Gen.change_my_city) 
        
@router.message(Gen.change_my_city)
async def change_my_city(msg: Message, state: FSMContext):
    json_data = json.load(open("db.json", encoding='utf8'))
    user_data = [i for i, data in enumerate(json_data) if data['user_id'] == msg.from_user.id]
    if user_data:
        user_data = json_data[user_data[0]]
        user_data['city'] = msg.text
        with open("db.json", "w") as outfile:
            json.dump(json_data, outfile, ensure_ascii=False)
        await msg.answer(text.change_interests.format(name=user_data['user_fullname'], city=msg.text))
        await state.set_state(Gen.change_interests) 


@router.message(Gen.change_interests)
async def change_my_city(msg: Message, state: FSMContext):
    json_data = json.load(open("db.json", encoding='utf8'))
    user_data = [i for i, data in enumerate(json_data) if data['user_id'] == msg.from_user.id]
    if user_data:
        user_data = json_data[user_data[0]]
        user_data['interest'] = re.split('\s+; |, |\*|\n| и ', msg.text)
        with open("db.json", "w") as outfile:
            json.dump(json_data, outfile, ensure_ascii=False)
        await msg.answer(text.change_info_done.format(name=user_data['user_fullname'], city=user_data['city'], interests=user_data['interest']))
        await state.set_state(Gen.initial_state) 

@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    json_data = json.load(open("db.json", encoding='utf8'))
    user_data = [i for i, data in enumerate(json_data) if data['user_id'] == msg.from_user.id]
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(mesg.text, userdata=[0])
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(prompt)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res[0] + text.text_watermark, disable_web_page_preview=True)


@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def generate_image(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.generate_image(prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)
