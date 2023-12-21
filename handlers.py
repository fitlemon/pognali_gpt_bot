from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
import json
import re


import kb
import text


from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import utils
import users
from states import Gen
import loader

router = Router()
bot = loader.bot


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
    await state.set_state(Gen.initial_state)  # change State to Initial State
    await msg.answer(text.menu, reply_markup=kb.menu_reg)  # Pop up menu
    # Create user if he doesnt exist
    if not await users.find_user(msg.from_user.id):
        data = users.dict_sample.copy()
        data["user_id"] = msg.from_user.id
        data["user_name"] = msg.from_user.username
        data["user_firstname"] = msg.from_user.full_name
        # initialize the dict of user profile

        await users.add_new_user_data(
            data, msg.from_user.id
        )  # add dict of user to json file


@router.callback_query(F.data == "main_menu")
async def menu_callback(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.initial_state)  # change State to Initial State
    await clbck.message.answer(text.menu, reply_markup=kb.menu_reg)  # Pop up menu


# Handler for catch "Where to go?!" button pushing
@router.callback_query(F.data == "where_to_go")
async def where_to_go(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.where_to_go)
    await clbck.message.answer(text.where_to_go, reply_markup=kb.where_to_go)


# Handler for catch "Events" button pushing
@router.callback_query(F.data == "events")
async def events_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events)
    await clbck.message.answer(text.events, reply_markup=kb.events)


# Handler for catch "Events by genres" button pushing
@router.callback_query(
    lambda call: call.data == "events_by_genre" or call.data == "events_by_genre_next"
)
async def events_by_genre_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_by_genre)
    tags = await utils.get_random_genres()
    tags_kb = []
    if tags is None:
        return None
    print(tags)
    for i in range(0, len(tags), 2):
        row = [
            InlineKeyboardButton(
                text=f"{tags[i][0]}", callback_data=f"events_by_genre_{tags[i][1]}"
            ),
            InlineKeyboardButton(
                text=f"{tags[i+1][0]}",
                callback_data=f"events_by_genre_{tags[i+1][1]}",
            ),
        ]
        tags_kb.append(row)
    next_random_kb = [
        InlineKeyboardButton(
            text="🔄 Посмотреть еще жанры",
            callback_data="events_by_genre_next",
        )
    ]
    tags_kb.append(next_random_kb)
    back_kb = [InlineKeyboardButton(text="⬅️ Назад", callback_data="events")]
    tags_kb.append(back_kb)
    tags_kb = InlineKeyboardMarkup(inline_keyboard=tags_kb)
    await clbck.message.edit_text(text.events_by_genre, reply_markup=tags_kb)


# Handler for catch "Specific genre" button pushing
@router.callback_query(F.data.contains("events_by_genre_"))
async def events_by_spec_genre(clbck: CallbackQuery, state: FSMContext):
    print(clbck.data)
    genre = clbck.data[16:]
    events_ids = await utils.get_upcoming_events_ids_by_tag(genre)
    if not events_ids:
        await clbck.message.answer("Мероприятия не найдены(", parse_mode="html")
        return None
    events = await utils.get_upcoming_events_with_tags_by_id(
        events_ids, ["title", "description", "start_date", "info_url", "price_from"]
    )  # get ids, *columns* tags from eventss
    intro = f"<b>Нашёл следующие мероприятия по жанру {genre}:</b>"
    message_text = []
    message_text.append(intro)
    if events:
        for enum, event in enumerate(events[:5]):
            print(event)
            message_text.append(f"🔸<b>{enum+1}</b>) <i>{event[1]}</i>.\n")
            if event[4]:
                message_text.append(f"🔗 Сайт для информации: {event[4]}\n")
            message_text.append(f"📅 Начало мероприятия: {event[3]}\n")
            if event[5]:
                message_text.append(f"💵 Цены от: {event[5]}\n")
            if event[6]:
                message_text.append(
                    f"""Tags: {str([f'#{str(tag).lower().replace(" ", "_").replace("-", "_")} ' for tag in event[6].split(', ')])}\n"""
                )
        offer_text = (
            "_" * 35
            + "\n"
            + "💡 Если не нашел подходящие именно тебе мероприятия...Расскажи немного о себе нейросети 💬. И она найдет тебе самые релевантные"
        )
        message_text.append(offer_text)
        full_kb = []
        offer_kb = [
            InlineKeyboardButton(text="👤 Рассказать о себе ИИ", callback_data="my_info")
        ]

        back_kb = [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="events_by_genre")
        ]

        full_kb.append(offer_kb)
        full_kb.append(back_kb)
        full_kb = InlineKeyboardMarkup(inline_keyboard=full_kb)
        await clbck.message.answer("\n".join(message_text), reply_markup=full_kb)
    else:
        await clbck.message.answer("Мероприятия не найдены(", parse_mode="html")


# Catch messagee in "Events by genre" state
@router.message(Gen.events_by_genre)
async def events_by_genre_user_query(msg: Message):
    """
    Handler that give events by user query in Events by genre state
    Args:
        msg (Message): User message
    """
    await msg.answer("🔎 Ищу мероприятия для тебя...")
    # upcoming_events = await utils.get_upcoming_events("description")  # get_text_from_events
    upcoming_events = await utils.get_events_tags()  # get events with their tags
    events_tags = [(id, tags) for id, name, tags in upcoming_events]
    print("Upcomin events:", upcoming_events)
    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    best_scored = await utils.rangeer(
        events_tags, msg.text
    )  # rangeer events with user text (Context recommendation)
    print("Best scored: ", best_scored)
    best_ids = tuple((id for id, tag, score in best_scored))
    if not best_ids:
        await msg.answer("Мероприятия не найдены(", parse_mode="html")
        return None
    events = await utils.get_upcoming_events_with_tags_by_id(
        best_ids, ["title", "description", "start_date", "info_url", "price_from"]
    )  # get ids, *columns* tags from eventss
    intro = f"<b>Нашёл следующие мероприятия по твоему запросу:</b>"
    message_text = []
    message_text.append(intro)
    if events:
        for enum, event in enumerate(events[:5]):
            print(event)
            message_text.append(f"🔸<b>{enum+1}</b>) <i>{event[1]}</i>.\n")
            if event[4]:
                message_text.append(f"🔗 Сайт для информации: {event[4]}\n")
            message_text.append(f"📅 Начало мероприятия: {event[3]}\n")
            if event[5]:
                message_text.append(f"💵 Цены от: {event[5]}\n")
            if event[6]:
                message_text.append(
                    f"""Tags: {str([f'#{str(tag).lower().replace(" ", "_").replace("-", "_")} ' for tag in event[6].split(', ')])}\n"""
                )

        offer_text = (
            "_" * 35
            + "\n"
            + "💡 Если не нашел подходящие именно тебе мероприятия...Расскажи немного о себе нейросети 💬. И она найдет тебе самые релевантные"
        )
        message_text.append(offer_text)
        full_kb = []
        offer_kb = [
            InlineKeyboardButton(text="👤 Рассказать о себе ИИ", callback_data="my_info")
        ]

        back_kb = [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="events_by_genre")
        ]

        full_kb.append(offer_kb)
        full_kb.append(back_kb)
        full_kb = InlineKeyboardMarkup(inline_keyboard=full_kb)
        await msg.answer("\n".join(message_text), reply_markup=full_kb)
    else:
        await msg.answer("Мероприятия не найдены(", parse_mode="html")


# Catch  "Events by desc" button
@router.callback_query(F.data == "events_by_desc")
async def events_by_user_query_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_by_desc)
    await clbck.message.answer(text.events_by_desc)


# Catch  "Events by desc" button
@router.message(Gen.events_by_desc)
async def events_by_genre_user_query(msg: Message):
    """
    Handler that give events by user query
    Args:
        msg (Message): User message
    """
    await msg.answer(
        "🔎 Ищу мероприятия для тебя по запросу: " + msg.text, parse_mode="html"
    )

    upcoming_events = await utils.get_upcoming_events_by_col(
        "description"
    )  # get events with their tags

    print("Upcomin events:", upcoming_events)
    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    best_scored = await utils.rangeer(
        upcoming_events, msg.text
    )  # rangeer events with user text (Context recommendation)
    print("Best scored: ", best_scored)
    best_ids = tuple((id for id, tag, score in best_scored))
    if not best_ids:
        await msg.answer("Мероприятия не найдены(", parse_mode="html")
        return None
    events = await utils.get_upcoming_events_with_tags_by_id(
        best_ids, ["title", "description", "start_date", "info_url", "price_from"]
    )  # get ids, *columns* tags from eventss
    intro = f"<b>Нашёл следующие мероприятия по твоему запросу:</b>"
    message_text = []
    message_text.append(intro)
    print("Incoming events:", events)
    if events:
        for enum, event in enumerate(events[:5]):
            print(event)
            message_text.append(f"🔸<b>{enum+1}</b>) <i>{event[1]}</i>.\n")
            if event[2]:
                message_text.append(
                    f'<i>{event[2].replace("<br>", "").replace("<p>", "").replace("</p>", "").replace("&nbsp;", "")}</i>.\n'
                )
            if event[4]:
                message_text.append(f"🔗 Сайт для информации: {event[4]}\n")
            message_text.append(f"📅 Начало мероприятия: {event[3]}\n")
            if event[5]:
                message_text.append(f"💵 Цены от: {event[5]}\n")
            if event[6]:
                message_text.append(
                    f"""Tags: {str([f'#{str(tag).lower().replace(" ", "_").replace("-", "_")} ' for tag in event[6].split(', ')])}\n"""
                )

        offer_text = (
            "_" * 35
            + "\n"
            + "💡 Если не нашел подходящие именно тебе мероприятия...Расскажи немного о себе нейросети 💬. И она найдет тебе самые релевантные"
        )
        message_text.append(offer_text)
        full_kb = []
        offer_kb = [
            InlineKeyboardButton(text="👤 Рассказать о себе ИИ", callback_data="my_info")
        ]

        back_kb = [InlineKeyboardButton(text="⬅️ Назад", callback_data="events")]

        full_kb.append(offer_kb)
        full_kb.append(back_kb)
        full_kb = InlineKeyboardMarkup(inline_keyboard=full_kb)
        await msg.answer("\n".join(message_text), reply_markup=full_kb)
    else:
        await msg.answer("Мероприятия не найдены(", parse_mode="html")


# Catch  "Events by desc and user data" button
@router.callback_query(F.data == "events_by_desc_and_user_data")
async def events_by_user_query_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_by_desc_and_user_data)
    await clbck.message.answer(text.events_by_desc_and_user_data)


# Catch  "Events by desc" button
@router.message(Gen.events_by_desc_and_user_data)
async def events_by_genre_user_query(msg: Message):
    """
    Handler that give events by user query and user data
    Args:
        msg (Message): User message
    """

    user_data = await users.get_user_data(msg.chat.id)

    # upcoming_events = await utils.get_upcoming_events("description")  # get_text_from_events
    need_text = [
        "main_music_genres",
        "favorite_techno_music",
        "favorite_main_music_artists",
        "favorite_techno_music_artists",
        "favorite_night_clubs",
        "favorite_bars",
        "favorite_djs",
        "current_location_address",
        "sex",
        "user_city",
    ]
    user_info_music = [
        ", ".join(value) if type(value) is list else str(value)
        for key, value in user_data.items()
        if key in need_text and value != "" and value != [] and value != "unknown"
    ]
    user_info_music = ", ".join(user_info_music)
    await msg.answer(
        "🔎 Ищу мероприятия для тебя по запросу: " + msg.text + ", " + user_info_music,
        parse_mode="html",
    )
    upcoming_events = await utils.get_upcoming_events_by_col(
        "description"
    )  # get events with their tags

    print("Upcomin events:", upcoming_events)
    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    best_scored = await utils.rangeer(
        upcoming_events, msg.text + ", " + user_info_music
    )  # rangeer events with user text (Context recommendation)
    print("Best scored: ", best_scored)
    best_ids = tuple((id for id, tag, score in best_scored))
    if not best_ids:
        await msg.answer("Мероприятия не найдены(", parse_mode="html")
        return None
    events = await utils.get_upcoming_events_with_tags_by_id(
        best_ids, ["title", "description", "start_date", "info_url", "price_from"]
    )  # get ids, *columns* tags from eventss
    intro = f"<b>Нашёл следующие мероприятия по твоему запросу и твоим интересам:</b>"
    message_text = []
    message_text.append(intro)
    print("Incoming events:", events)
    if events:
        for enum, event in enumerate(events[:5]):
            print(event)
            message_text.append(f"🔸<b>{enum+1}</b>) <i>{event[1]}</i>.\n")
            if event[2]:
                message_text.append(
                    f'<i>{event[2].replace("<br>", "").replace("<p>", "").replace("</p>", "").replace("&nbsp;", "")}</i>.\n'
                )
            if event[4]:
                message_text.append(f"🔗 Сайт для информации: {event[4]}\n")
            message_text.append(f"📅 Начало мероприятия: {event[3]}\n")
            if event[5]:
                message_text.append(f"💵 Цены от: {event[5]}\n")
            if event[6]:
                message_text.append(
                    f"""Tags: {str([f'#{str(tag).lower().replace(" ", "_").replace("-", "_")} ' for tag in event[6].split(', ')])}\n"""
                )

        offer_text = (
            "_" * 35
            + "\n"
            + "💡 Если не нашел подходящие именно тебе мероприятия...Расскажи немного о себе нейросети 💬. И она найдет тебе самые релевантные"
        )
        message_text.append(offer_text)
        full_kb = []
        offer_kb = [
            InlineKeyboardButton(text="👤 Рассказать о себе ИИ", callback_data="my_info")
        ]

        back_kb = [InlineKeyboardButton(text="⬅️ Назад", callback_data="events")]

        full_kb.append(offer_kb)
        full_kb.append(back_kb)
        full_kb = InlineKeyboardMarkup(inline_keyboard=full_kb)
        await msg.answer("\n".join(message_text), reply_markup=full_kb)
    else:
        await msg.answer("Мероприятия не найдены(", parse_mode="html")


# Handler for catch "Events by location" button pushing
@router.callback_query(F.data == "events_by_location")
async def events_by_location_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_by_location)
    await clbck.message.answer(text.events_by_location)
    await state.set_state(Gen.events_by_genre)
    tags = await utils.get_random_genres()


# Handler for catch "Popular events" button pushing
@router.callback_query(F.data == "events_popular")
async def events_popular_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_popular)
    await clbck.message.answer(text.events_popular)


# Handler for catch "Recommended events" button pushing
@router.callback_query(F.data == "events_recomend_by_desc")
async def events_recomend_by_desc_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_recomend)
    """
    Handler that give events match to user data by desc 
    
    """

    user_data = await users.get_user_data(clbck.message.chat.id)

    # upcoming_events = await utils.get_upcoming_events("description")  # get_text_from_events
    need_text = [
        "main_music_genres",
        "favorite_techno_music",
        "favorite_main_music_artists",
        "favorite_techno_music_artists",
        "favorite_night_clubs",
        "favorite_bars",
        "favorite_djs",
        "current_location_address",
        "sex",
        "user_city",
    ]
    user_info_music = [
        ", ".join(value) if type(value) is list else str(value)
        for key, value in user_data.items()
        if key in need_text and value != "" and value != [] and value != "unknown"
    ]
    user_info_music = ", ".join(user_info_music)
    await clbck.message.answer(
        "🔎 Ищу мероприятия по твоим интересам:" + user_info_music, parse_mode="html"
    )
    upcoming_events = await utils.get_upcoming_events_by_col(
        "description"
    )  # get events with their tags

    print("Upcomin events:", upcoming_events)
    await bot.send_chat_action(chat_id=clbck.message.chat.id, action="typing")
    best_scored = await utils.rangeer(
        upcoming_events, user_info_music
    )  # rangeer events with user text (Context recommendation)
    print("Best scored: ", best_scored)
    best_ids = tuple((id for id, tag, score in best_scored))
    if not best_ids:
        await clbck.message.answer("Мероприятия не найдены(", parse_mode="html")
        return None
    events = await utils.get_upcoming_events_with_tags_by_id(
        best_ids, ["title", "description", "start_date", "info_url", "price_from"]
    )  # get ids, *columns* tags from eventss
    intro = f"<b>Нашёл следующие мероприятия по твоему запросу:</b>"
    message_text = []
    message_text.append(intro)
    print("Incoming events:", events)
    if events:
        for enum, event in enumerate(events[:5]):
            print(event)
            message_text.append(f"🔸<b>{enum+1}</b>) <i>{event[1]}</i>.\n")
            if event[2]:
                message_text.append(
                    f'<i>{event[2].replace("<br>", "").replace("<p>", "").replace("</p>", "").replace("&nbsp;", "")}</i>.\n'
                )
            if event[4]:
                message_text.append(f"🔗 Сайт для информации: {event[4]}\n")
            message_text.append(f"📅 Начало мероприятия: {event[3]}\n")
            if event[5]:
                message_text.append(f"💵 Цены от: {event[5]}\n")
            if event[6]:
                message_text.append(
                    f"""Tags: {str([f'#{str(tag).lower().replace(" ", "_").replace("-", "_")} ' for tag in event[6].split(', ')])}\n"""
                )

        offer_text = (
            "_" * 35
            + "\n"
            + "💡 Если не нашел подходящие именно тебе мероприятия...Расскажи немного о себе нейросети 💬. И она найдет тебе самые релевантные"
        )
        message_text.append(offer_text)
        full_kb = []
        regenerate_kb = [
            InlineKeyboardButton(
                text="🔄 Посмотреть другие варианты",
                callback_data="events_recomend_by_desc",
            )
        ]
        offer_kb = [
            InlineKeyboardButton(text="👤 Рассказать о себе ИИ", callback_data="my_info")
        ]

        back_kb = [InlineKeyboardButton(text="⬅️ Назад", callback_data="events")]
        full_kb.append(regenerate_kb)
        full_kb.append(offer_kb)
        full_kb.append(back_kb)
        full_kb = InlineKeyboardMarkup(inline_keyboard=full_kb)
        await clbck.message.answer("\n".join(message_text), reply_markup=full_kb)
    else:
        await clbck.message.answer("Мероприятия не найдены(", parse_mode="html")


# Handler for catch "Recommended events" button pushing
@router.callback_query(F.data == "events_recomend_by_desc_tags")
async def events_recommend_by_desc_tags_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.events_recomend)
    """
    Handler that give events match to user data by desc and tags

    """

    user_data = await users.get_user_data(clbck.message.chat.id)
    # upcoming_events = await utils.get_upcoming_events("description")  # get_text_from_events
    need_text = [
        "main_music_genres",
        "favorite_techno_music",
        "favorite_main_music_artists",
        "favorite_techno_music_artists",
        "favorite_night_clubs",
        "favorite_bars",
        "favorite_djs",
        "current_location_address",
        "sex",
        "user_city",
    ]
    user_info_music = [
        ", ".join(value) if type(value) is list else str(value)
        for key, value in user_data.items()
        if key in need_text and value != "" and value != [] and value != "unknown"
    ]
    user_info_music = ", ".join(user_info_music)
    await clbck.message.answer(
        "🔎 Ищу мероприятия по твоим интересам:" + user_info_music, parse_mode="html"
    )
    upcoming_events = await utils.get_upcoming_events_with_tags(
        "description"
    )  # get events with their tags
    upcoming_events = [[ids, desc + ", " + tag] for ids, desc, tag in upcoming_events]

    print("Upcomin events:", upcoming_events)
    await bot.send_chat_action(chat_id=clbck.message.chat.id, action="typing")
    best_scored = await utils.rangeer(
        upcoming_events, user_info_music
    )  # rangeer events with user text (Context recommendation)
    print("Best scored: ", best_scored)
    best_ids = tuple((id for id, tag, score in best_scored))
    if not best_ids:
        await clbck.message.answer("Мероприятия не найдены(", parse_mode="html")
        return None
    events = await utils.get_upcoming_events_with_tags_by_id(
        best_ids, ["title", "description", "start_date", "info_url", "price_from"]
    )  # get ids, *columns* tags from eventss
    intro = f"<b>Нашёл следующие мероприятия по твоему запросу:</b>"
    message_text = []
    message_text.append(intro)
    print("Incoming events:", events)
    if events:
        for enum, event in enumerate(events[:5]):
            print(event)
            message_text.append(f"🔸<b>{enum+1}</b>) <i>{event[1]}</i>.\n")
            if event[2]:
                message_text.append(
                    f'<i>{event[2].replace("<br>", "").replace("<p>", "").replace("</p>", "").replace("&nbsp;", "")}</i>.\n'
                )
            if event[4]:
                message_text.append(f"🔗 Сайт для информации: {event[4]}\n")
            message_text.append(f"📅 Начало мероприятия: {event[3]}\n")
            if event[5]:
                message_text.append(f"💵 Цены от: {event[5]}\n")
            if event[6]:
                message_text.append(
                    f"""Tags: {str([f'#{str(tag).lower().replace(" ", "_").replace("-", "_")} ' for tag in event[6].split(', ')])}\n"""
                )

        offer_text = (
            "_" * 35
            + "\n"
            + "💡 Если не нашел подходящие именно тебе мероприятия...Расскажи немного о себе нейросети 💬. И она найдет тебе самые релевантные"
        )
        message_text.append(offer_text)
        full_kb = []
        regenerate_kb = [
            InlineKeyboardButton(
                text="🔄 Посмотреть другие варианты",
                callback_data="events_recomend_by_desc_tags",
            )
        ]
        offer_kb = [
            InlineKeyboardButton(text="👤 Рассказать о себе ИИ", callback_data="my_info")
        ]

        back_kb = [InlineKeyboardButton(text="⬅️ Назад", callback_data="events")]
        full_kb.append(regenerate_kb)
        full_kb.append(offer_kb)
        full_kb.append(back_kb)
        full_kb = InlineKeyboardMarkup(inline_keyboard=full_kb)
        await clbck.message.answer("\n".join(message_text), reply_markup=full_kb)
    else:
        await clbck.message.answer("Мероприятия не найдены(", parse_mode="html")


# Handler for catch "Venues" button pushing
@router.callback_query(F.data == "venues")
async def venues_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.venues)
    await clbck.message.answer(text.venues, reply_markup=kb.venues)


# Handler for catch "Venues by genres" button pushing
@router.callback_query(F.data == "venues_by_genre")
async def venues_by_genre_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.venues_by_genre)
    await clbck.message.answer(text.venues_by_genre)


# Handler for catch "Venues by location" button pushing
@router.callback_query(F.data == "venues_by_location")
async def venues_by_location_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.venues_by_location)
    await clbck.message.answer(text.venues_by_location)


# Handler for catch "Popular Venues" button pushing
@router.callback_query(F.data == "venues_popular")
async def venues_popular_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.venues_popular)
    await clbck.message.answer(text.venues_popular)


# Handler for catch "Recomended Venues" button pushing
@router.callback_query(F.data == "venues_recomend")
async def venues_recomend_menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.venues_recomend)
    await clbck.message.answer(text.venues_recomend)


@router.callback_query(F.data == "pognali")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.pognali)
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
    await bot.send_chat_action(chat_id=clbck.message.chat.id, action="typing")
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
    await bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    res = await utils.prompt_to_dude(msg.text, user_data)
    await msg.answer(res[0] + text.text_watermark, disable_web_page_preview=True)
    dict_res = await utils.prompt_to_dict_changer(msg.text, user_data)
    print(f"RETURN DICT TO HANDLER:{dict_res}")

    if type(dict_res) is dict:
        await users.update_user_data(dict_res, msg.from_user.id)
    await msg.answer(str(dict_res) + text.text_watermark, disable_web_page_preview=True)
    if res:
        await users.add_last_question(res[0], msg.from_user.id)
