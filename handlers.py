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
import users
from states import Gen

router = Router()


# Handler for start command at the beginning
@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    """
    Bot actions for start command
    """
    await msg.answer(
        text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu_reg
    )  # Greeting message to user
    data = users.dict_sample.copy()
    data["user_id"] = msg.from_user.id
    data["user_name"] = msg.from_user.username
    data["user_firstname"] = msg.from_user.full_name
    # initialize the dict of user profile

    await users.add_new_user_data(
        data, msg.from_user.id
    )  # add dict of user to json file
    await state.set_state(Gen.initial_state)  # change State to Initial State


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
@router.message(Command("menu"))
async def menu(msg: Message, state: FSMContext):
    await msg.answer(
        "Выходим в главное меню...", reply_markup=ReplyKeyboardRemove()
    )  # Remove Keyboard
    await state.set_state(Gen.initial_state)  # change State to Initial State
    await msg.answer(text.menu, reply_markup=kb.menu_reg)  # Pop up menu


# Handler for catch "Where to go?!" button pushing


@router.callback_query(F.data == "my_city_events")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.event_list_prompt)
    await clbck.message.answer(text.gen_text)
    # await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    user_data = await users.get_user_data(clbck.message.chat.id)
    res = await utils.generate_events_list(user_data)
    if not res:
        return await clbck.message.answer(text.gen_error, reply_markup=kb.exit_kb)

    await clbck.message.answer(
        res[0] + text.text_watermark,
        disable_web_page_preview=True,
        reply_markup=kb.update_info,
    )
    await state.set_state(Gen.text_prompt)


# Handler for "Change my info" button
@router.callback_query(F.data == "my_info")
async def request_for_change_my_info(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.update_info)
    user_data = await users.get_user_data(clbck.message.chat.id)
    await clbck.message.answer(text.gen_text)
    question = "Я рад снова вернуться на интервью!"
    await users.add_last_question(question, clbck.message.chat.id)
    user_data["last_question"] = question
    # res = await utils.update_info_prompt("Расскажи что ты знаешь обо мне. А потом продолжай задавать вопросы", user_data)
    res = await utils.prompt_to_dude("Я хочу рассказать немного о себе.", user_data)
    if not res:
        return await clbck.message.answer(text.gen_error)
    try:
        question = res[0]
        await users.add_last_question(question, clbck.message.chat.id)
        await clbck.message.answer(
            res[0] + text.text_watermark, disable_web_page_preview=True
        )

    except:
        await clbck.message.answer(text.gen_error, reply_markup=kb.exit_kb)


## Handler for messages in "Update info" State
@router.message(Gen.update_info)
async def change_my_info(msg: Message, state: FSMContext):
    await state.set_state(Gen.update_info)
    user_data = await users.get_user_data(msg.from_user.id)
    await msg.answer(text.gen_text)
    # res = await utils.update_info_prompt(msg.text, user_data)
    res = await utils.prompt_to_dude(msg.text, user_data)
    await msg.answer(res[0] + text.text_watermark, disable_web_page_preview=True)
    dict_res = await utils.prompt_to_dict_changer(msg.text, user_data)
    print(f"RETURN DICT TO HANDLER:{dict_res}")

    if type(dict_res) is dict:
        await users.update_user_data(dict_res, msg.from_user.id)
    await msg.answer(str(dict_res) + text.text_watermark, disable_web_page_preview=True)
    if res:
        await users.add_last_question(res[0], msg.from_user.id)
