from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


menu_intro = [
    [InlineKeyboardButton(text="📝👤 Заполнить инфо о себе", callback_data="fill_info"),],
]
menu_reg = [
    [InlineKeyboardButton(text="🎉 Куда сходить на выходных?!", callback_data="my_city_events"),],    
    [InlineKeyboardButton(text="🗼 Я в другом городе. Куда сходить?!", callback_data="another_city"),],
    [InlineKeyboardButton(text="🏁 Сгенерировать квесты в городе", callback_data="gen_quests")],
    [InlineKeyboardButton(text="👤 Заполнить инфо о себе?!", callback_data="my_info")],
    [InlineKeyboardButton(text="🔎 Помощь?!", callback_data="help"),
     InlineKeyboardButton(text="📄 Информация?!", callback_data="about_us"),]
]

change_info_kb = [
    [InlineKeyboardButton(text="Заполнить информацию о себе", callback_data="change_my_info"),],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu"),],
    ]

change_my_city_kb = [
    [KeyboardButton(text="Отправить геолокацию", request_location=True)],
    [KeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]
    
exit_button= [[KeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]]

menu_intro = InlineKeyboardMarkup(inline_keyboard=menu_intro)
menu_reg = InlineKeyboardMarkup(inline_keyboard=menu_reg)
exit_kb = ReplyKeyboardMarkup(keyboard=exit_button, resize_keyboard=True)
change_info_kb = InlineKeyboardMarkup(inline_keyboard=change_info_kb)

change_my_city_kb = ReplyKeyboardMarkup(keyboard=change_my_city_kb, resize_keyboard=True)
