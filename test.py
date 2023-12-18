import json
import re
from pprint import pprint

st = """{"content": "\u041f\u0440\u0438\u0432\u0435\u0442, Davron! \u0420\u0430\u0434 \u043f\u043e\u0437\u043d\u0430\u043a\u043e\u043c\u0438\u0442\u044c\u0441\u044f \u0441 \u0442\u043e\u0431\u043e\u0439. \u042f \u0437\u0430\u043c\u0435\u0447\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u0441\u043f\u0440\u0430\u0432\u043b\u044f\u044e\u0441\u044c \u0441 \u043f\u043e\u0438\u0441\u043a\u043e\u043c \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u044b\u0445 \u043c\u0435\u0441\u0442 \u0438 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u0439. \u0420\u0430\u0441\u0441\u043a\u0430\u0436\u0438, \u0447\u0442\u043e \u0442\u0435\u0431\u044f \u0431\u043e\u043b\u044c\u0448\u0435 \u0432\u0441\u0435\u0433\u043e \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u0443\u0435\u0442: \u0442\u0435\u0430\u0442\u0440\u044b, \u043a\u0438\u043d\u043e\u0442\u0435\u0430\u0442\u0440\u044b, \u0434\u043e\u0441\u0442\u043e\u043f\u0440\u0438\u043c\u0435\u0447\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u0438\u043b\u0438 \u0447\u0442\u043e-\u0442\u043e \u0435\u0449\u0435? \u0418 \u0435\u0441\u043b\u0438 \u0435\u0441\u0442\u044c \u043a\u0430\u043a\u0438\u0435-\u0442\u043e \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u044b\u0435 \u043f\u0440\u0435\u0434\u043f\u043e\u0447\u0442\u0435\u043d\u0438\u044f, \u043d\u0430\u043f\u0440\u0438\u043c\u0435\u0440, \u0436\u0430\u043d\u0440\u044b \u0444\u0438\u043b\u044c\u043c\u043e\u0432 \u0438\u043b\u0438 \u0432\u0438\u0434\u044b \u0441\u043f\u043e\u0440\u0442\u0430, \u0442\u043e \u043f\u043e\u0434\u0435\u043b\u0438\u0441\u044c \u0438\u043c\u0438 \u0441\u043e \u043c\u043d\u043e\u0439. \u0427\u0442\u043e\u0431\u044b \u043c\u043d\u0435 \u0431\u044b\u043b\u043e \u043b\u0435\u0433\u0447\u0435 \u043d\u0430\u0439\u0442\u0438 \u0442\u043e, \u0447\u0442\u043e \u0442\u0435\u0431\u0435 \u043f\u043e\u043d\u0440\u0430\u0432\u0438\u0442\u0441\u044f! \ud83d\ude0a",
  "role": "assistant"
}"""
st = st.encode("utf-16", "surrogatepass").decode("utf-16")
d_data = json.loads(st.replace("'", '"'))

# st2 = "\ud83d\ude04".encode('utf-16','surrogatepass').decode('utf-16')
# print(st2)
import re

text = "Конечно, вот обновленный словарь с заполненными ключевыми словами: \n \
# \n\
# my_info_dict вфавфафа= вфв{'user_id': 400690372, 'user_name': 'ihmatullaev', 'user_firstname': 'Davron', 'user_surname': '', 'age': 0, 'sex': '', 'about_me': ['new user'], 'topics_history': ['Твои любимые фильмы'], 'favorite_films': ['Титаник'], 'favorite_books': [''], 'favorite_shows': [''], 'favorite_sports': [''], 'favorite_countries': [''], 'favorite_cities': [''], 'favorite_youtube_channels': [''], 'user_city': 'unknown', 'user_interests': [''], 'last_question': 'Привет, Даврон! Спасибо за комментарий по поводу предыдущего ответа. Я действительно хотел бы узнать о тебе больше, поэтому давай продолжим наше интервью. \n\nИтак, перейдем к следующей теме. Я вижу, что у тебя есть интересы в фильмах. Какие жанры или фильмы ты предпочитаешь смотреть? Может быть, у тебя есть любимые актеры или актрисы? Я бы хотел узнать больше о твоих предпочтениях в кино. Расскажи мне о том, что ты наслаждаешься в фильмах, чтобы я мог обновить информацию в словаре.'}"
# pattern = re.compile(r"({[^}]*})", re.DOTALL)
# match = pattern.search(text)

# if match:
#     dictionary_text = match.group(1)
#     print(dictionary_text)

# data = "{'user_id': 400690372, 'user_name': 'ihmatullaev', 'user_firstname': 'Davron', 'user_surname': '', 'age': 0, 'sex': 'male', 'user_city': '', 'misc_data': {'about_me': ['new user', 'Мне нравится техно.'], 'favorite_books': [''], 'favorite_films': [''], 'favorite_shows': [''], 'topics_history': [''], 'user_interests': ['Мне нравится техно.'], 'favorite_cities': [''], 'favorite_sports': [''], 'favorite_countries': [''], 'favorite_youtube_channels': ['']}}"
# print(data[116:119])
# try:
#     json_data = json.loads(data.replace("'",'"'))
#     print(json_data)
# except json.JSONDecodeError as e:
#     print("Invalid JSON syntax:", e)


dict_sample = {
    "user_id": 1,
    "user_name": "Test",
    "user_firstname": "Test",
    "user_surname": "",
    "age": 0,
    "sex": "",
    "user_city": "",
    "last_question": "",
    "misc_data": {
        "about_me": ["new user"],
        "topics_history": [""],
        "favorite_films": [""],
        "favorite_books": [""],
        "favorite_shows": [""],
        "favorite_sports": [""],
        "favorite_countries": [""],
        "favorite_cities": [""],
        "favorite_youtube_channels": [""],
        "user_interests": [""],
    },
}

dict2 = {
    "user_id": 400690372,
    "user_name": "ihmatullaev",
    "user_firstname": "Davron",
    "user_surname": "",
    "age": 0,
    "sex": "",
    "user_city": "",
    "misc_data": {
        "about_me": ["new user"],
        "favorite_books": [""],
        "favorite_films": [""],
        "favorite_shows": [""],
        "topics_history": [""],
        "user_interests": [""],
        "favorite_cities": [""],
        "favorite_sports": [""],
        "favorite_countries": [""],
        "favorite_youtube_channels": [""],
    },
    "my_interests": "",
    "my_favorite_things": "",
    "interviewee_info": "Хочу в клуб",
    "my_city": "",
    "favorite_sports": "",
    "favorite_countries": "",
    "favorite_cities": "",
    "user_interests": "",
    "topics_history": "",
    "about_me": "",
}
# dict1.update((k, dict2[k]) for k in set(dict2).intersection(dict1))
# pprint(dict1)

user_data = {
    "user_id": 400690372,
    "user_name": "ihmatullaev",
    "user_firstname": "Davron",
    "user_surname": "",
    "age": 30,
    "sex": "",
    "user_city": "",
    "misc_data": {
        "about_me": ["new user", "мне 30"],
        "favorite_books": [""],
        "favorite_films": [""],
        "favorite_shows": [""],
        "topics_history": [""],
        "user_interests": [""],
        "favorite_cities": [""],
        "favorite_sports": [""],
        "favorite_countries": [""],
        "favorite_youtube_channels": [""],
    },
    "last_question": "Благодарю за продолжение интервью и за предоставленную информацию! 😊🎉\n\nТак как у тебя отсутствует фамилия, я бы хотел узнать, имеешь ли ты в наличии фамилию, которую ты мог бы поделиться? 🧐\n\nОтносительно Лондона, это отличный город! Если тебе нравится Лондон, то, возможно, у тебя есть и другие любимые города. Мог бы ты поделиться ими со мной? 🌍\n\nТакже, меня интересуют твои предпочтения в фильмах и сериалах. Можешь ли рассказать мне о том, какие фильмы или сериалы тебе особенно нравятся? 🎥📺\n\nИ, конечно, если у тебя есть какие-либо интересы, о которых ты хотел бы рассказать, буду рад услышать о них! 🎶\n\nЕсли в моем предыдущем вопросе я не был достаточно конкретен или если у тебя есть дополнительная информация, которой ты можешь поделиться, пожалуйста, сообщи мне! 😊\n\nОжидаю твоих отв,\
етов! 🎉,\
",
}
# col_val = [
#     f"{key} = {value}"
#     for key, value in user_data.items()
#     if value != None and value != "" and key != "user_id"
# ]
# print(f"\nColumn and values for update: {col_val}\n")
# # query = ", ".join(col_val)
# query = (
#     """update public.users set """ + ", ".join(col_val) + " where user_id=" + str(12)
# )
# print(query)

dict_sample = {
    "user_id": 1,
    "user_name": "Test",
    "user_firstname": "Test",
    "user_surname": "unknown",
    "age": 0,
    "sex": "unknown",
    "user_city": "unkown",
    "main_music_genres": {""},
    "techno_music_genres": {""},
    "favorite_techno_music_artists": {""},
    "favorite_night_clubs": {""},
    "favorite_bars": {""},
    "current_location_address": {""},
    "current_location_coordinates": (0, 0),
    "last_question": "unknown",
}
columns = "(" + ", ".join([key for key in dict_sample.keys()]) + ")"
values = ", ".join([str(value) for value in dict_sample.values()])
query = "INSERT INTO public.users " + columns + " VALUES " + values
# print(query)
test = """{'user_id': 400690372, 'user_name': 'ihmatullaev', 'user_firstname': 'Davron', 'user_surname': 'unknown', 'age': 0, 'sex': 'unknown', 'user_city': 'unknown', 'main_music_genres': [''], 'techno_music_genres': [''], 'favorite_techno_music_artists': [''], 'favorite_night_clubs': [''], 'favorite_bars': [''], 'current_location_address': [''], 'current_location_coordinates': '(0,0)'}"""
print(test[325:339])
print(test.replace("'", '"'))
try:
    json_data = json.loads(test.replace("'", '"'))
    print(json_data)
except json.JSONDecodeError as e:
    print("Invalid JSON syntax:", e)
