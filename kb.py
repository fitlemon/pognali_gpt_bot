from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


menu_intro = [
    [
        InlineKeyboardButton(
            text="📝👤 Заполнить инфо о себе", callback_data="fill_info"
        ),
    ],
]
# menu_reg = [
#     [InlineKeyboardButton(text="
#     [InlineKeyboardButton(text="🗼 Я в другом городе. Куда сходить?!", callback_data="another_city"),],
#     [InlineKeyboardButton(text="🏁 Сгенерировать квесты в городе", callback_data="gen_quests")],
#     [InlineKeyboardButton(text="👤 Заполнить инфо о себе?!", callback_data="my_info")],
#     [InlineKeyboardButton(text="🔎 Помощь?!", callback_data="help"),
#      InlineKeyboardButton(text="📄 Информация?!", callback_data="about_us"),]
# ]
menu_reg = [
    [InlineKeyboardButton(text="🎉 Ну че, погнали?!", callback_data="where_to_go")],
    [InlineKeyboardButton(text="👤 Заполнить инфо о себе", callback_data="my_info")],
    [
        InlineKeyboardButton(text="🔎 Помощь", callback_data="help"),
        InlineKeyboardButton(
            text="📄 Информация",
            callback_data="about_us",
        ),
    ],
]

exit_button = [[KeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]]

menu_intro = InlineKeyboardMarkup(inline_keyboard=menu_intro)
menu_reg = InlineKeyboardMarkup(inline_keyboard=menu_reg)
exit_kb = ReplyKeyboardMarkup(keyboard=exit_button, resize_keyboard=True)

update_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👤 Рассказать о себе?!", callback_data="my_info")]
    ]
)

where_to_go = [
    [InlineKeyboardButton(text="🎉 Мероприятия", callback_data="events")],
    [
        InlineKeyboardButton(text="📍 Заведения", callback_data="venues"),
    ],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")],
]
where_to_go = InlineKeyboardMarkup(inline_keyboard=where_to_go)

events = [
    [
        InlineKeyboardButton(
            text="🎵 Мероприятия по жанрам", callback_data="events_by_genre"
        )
    ],
    [
        InlineKeyboardButton(
            text="✏️ Мероприятия по запросу", callback_data="events_by_desc"
        )
    ],
    [
        InlineKeyboardButton(
            text="✏️ 👤 Мероприятия по запросу и интересам",
            callback_data="events_by_desc_and_user_data",
        )
    ],
    [
        InlineKeyboardButton(
            text="🚩 Мероприятия поблизости", callback_data="events_by_location"
        )
    ],
    [
        InlineKeyboardButton(
            text="⭐ Популярные мероприятия", callback_data="events_popular"
        )
    ],
    [
        InlineKeyboardButton(
            text="💚 Рекомендованные мне (описание)",
            callback_data="events_recomend_by_desc",
        )
    ],
    [
        InlineKeyboardButton(
            text="💚 Рекомендованные мне (описания+тэги) #️⃣ ",
            callback_data="events_recomend_by_desc_tags",
        )
    ],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="where_to_go")],
]

events = InlineKeyboardMarkup(inline_keyboard=events)


venues = [
    [
        InlineKeyboardButton(
            text="🎵 Заведения по жанрам", callback_data="venues_by_genre"
        )
    ],
    [
        InlineKeyboardButton(
            text="🚩 Заведения поблизости", callback_data="venues_by_location"
        )
    ],
    [
        InlineKeyboardButton(
            text="⭐ Популярные заведения", callback_data="venues_popular"
        )
    ],
    [
        InlineKeyboardButton(
            text="💚 Рекомендованные мне", callback_data="venues_recomend"
        )
    ],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="where_to_go")],
]

venues = InlineKeyboardMarkup(inline_keyboard=venues)
