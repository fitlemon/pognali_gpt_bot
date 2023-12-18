import openai
import logging
import config
import datetime
import json
from pprint import pprint
from environs import Env

# import env config file
env = Env()
env.read_env()

openai.api_key = env("OPENAI_TOKEN")
max_token_count = 4096
logging.basicConfig(
    filename="logging.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

# async def update_info_prompt(prompt, userdata) -> dict:
#     try:
#         intro_rule = "Ты интервьюер, ты интересуешься мной и постоянно задаешь вопросы. Вот наш прошлый разговор:\n\n"
#         question = f" Твой последний вопрос: {userdata['last_question']} \n"
#         user_message = f"\n Вот мой ответ на твой вопрос: {prompt}. \n"
#         user_dict =f"Есть Python словарь с данными обо мне, который ты должен заполнить. \n \
#             Проанализируй свой вопрос и мой ответ и заполни этот словарь, чтобы больше обо мне знать. \n \
#             Вот твой Python словарь с информацией обо мне, который ты обязан заполнить: \n my_dict = {userdata} \n"
#         final_rule = "Дай комментарий на мой прошлый ответ. Смени деликатно тему. Сформулируй следующий вопрос на другую тему, чтобы заполнить словарь дальше. \n \
#         \n \
#         Если мой ответ был не в тему вопроса. Скажи что твоя задача узнать обо мне больше, и хотел бы чтобы я тебе отвечал на вопросы. \n \
#         Или попросил сменить тему. Можешь даже переспрашивать информацию из словаря, уточняя ее актуальность . Будь веселым и можешь добавлять шутки к моим ответам. Сменяй темы разговоров. Главное чтобы заполнить недостающую информацию в твоем словаре. Не здаровайся. Мы давно уже общаемся. "
#         remind_dict = ' и Прикрепи к своему следующему вопросу словарь с заполненными ключевыми словами и без комментариев и без лишних слов. Только словарь!! \n \
#                     \n Не забудь обновить все ключи, особенно user_interests - мои интересы, topics_history - тема нашего прошлого разговора. \n \
#                         \n Не создавай новые ключи.\n \
#                         Отправляй в формате: my_info_dict = обновлённый словарь. ОБНОВИ КЛЮЧИ!!'
#         full_message = [{"role": "user", "content": intro_rule + question + user_message + user_dict + final_rule + remind_dict}]


#         response = await openai.ChatCompletion.acreate(
#             model="gpt-3.5-turbo",
#             messages=full_message
#         )
#         if response['usage']['total_tokens'] >= max_token_count:
#             return None
#         return response['choices'][0]['message']['content'] , full_message, response['usage']['total_tokens']
#     except Exception as e:
#         logging.error(e)


async def prompt_to_dude(prompt, userdata) -> dict:
    try:
        last_question = userdata["last_question"]
        del userdata["last_question"]
        intro_rule = "Ты мой друг (бро)!! Я твой лучший друг (бро)!! Ты берешь у меня интервью уже пол часа. Ты задаешь мне вопросы, я на них отвечаю. Ты должен узнать какие ночные клубы, мероприятия мне нравятся. Какой жанр музыки, особенно в техно направлении, мне нравится"
        question = f"Вот твой последний вопрос:  {last_question} \n"
        user_message = f"\n Вот мой ответ на этот вопрос:  {prompt}. \n"
        user_dict = f"Также я тебе дам  Python словарь, где приведена информация которой ты обладаешь обо мне на текущий момент.:  \n \
                   ```{userdata}```\n"
        final_rule = "Твои следующие действия: \n1) Расскажи шутку о тусовках и прочее. (Never say me Hello).\n 2)  Прокомментируй мой ответ: если он был по теме твоего вопроса, то задавай уточняющий вопрос, если нужно, если нет то смени тему чтобы заполнить другую информацию обо мне (например, мой возраст, пол, мои любимые музыкальные жанры, техно жанры, любимые техно-артисты, любимые ночные клубы, бары, тусовки). если ответ был не потеме твоего вопроса, то отшутись по этому поводу и задай другой вопрос по теме \n 4) Если есть какая то информация в словаре, уточни эту информацию обо мне (например, мои любимые музыкальные жанры, техно жанры, любимые техно-артисты, любимые ночные клубы, бары, тусовки) \n P.S.: Добавляй emojies в свой текст"
        full_message = [
            {
                "role": "user",
                "content": intro_rule
                + question
                + user_message
                + user_dict
                + final_rule,
            }
        ]

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo", messages=full_message
        )
        userdata["last_question"] = last_question

        print(f"\n\nASK QUESTION: \n\n {full_message}")
        if response["usage"]["total_tokens"] >= max_token_count:
            return None

        return (
            response["choices"][0]["message"]["content"],
            full_message,
            response["usage"]["total_tokens"],
        )
    except Exception as e:
        logging.error(e)


async def prompt_to_dict_changer(prompt, userdata) -> dict:
    try:
        last_question = userdata["last_question"]
        del userdata["last_question"]
        print(f"\n\nINTRO DICT\n\n:{userdata}")
        intro_rule = "Receive a snippet of an interview: journalist's question and interviewee's answer. Also, get the interviewee's profile dictionary. Fill in the user's profile as a dictionary using the question and answer. Update only existing keys, do not create new ones. Send me only the updated dictionary!"
        question = f"Journalist's question:  {last_question} \n"
        user_message = f"\n \n Interviewee's answer to this question:   {prompt}. \n"
        user_dict = f"User data dictionary: \n \
                   ```{userdata}```\n"
        final_rule = "Your actions: 1) Extract keywords (my favorite music_genres, techno_music_genres, favorite_techno_music_artists, favorite_night_clubs, favorite_bars, current_location_address) from the answer. 2) Update dictionary items with the found information (Only update existing keys like a age, sex, music_genres, techno_music_genres, favorite_techno_music_artists, favorite_night_clubs, favorite_bars, current_location_address)  4) Don't create new keys in dictionary. 3) Send me the updated dictionary in the format \{new_dict\}. Nothing extra!"
        full_message = [
            {
                "role": "user",
                "content": intro_rule
                + question
                + user_message
                + user_dict
                + final_rule,
            }
        ]
        print(f"\n\nASK DICT\n\n:{full_message}")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo", messages=full_message
        )
        if response["usage"]["total_tokens"] >= max_token_count:
            return None

        print(
            f"\n\nRESPONSE FROM GPT:\n\n {response['choices'][0]['message']['content']}"
        )
        try:
            json_data = json.loads(
                response["choices"][0]["message"]["content"].replace("'", '"')
            )
            print(json_data)
        except json.JSONDecodeError as e:
            print("Invalid JSON syntax:", e)
        json_data["last_question"] = last_question
        return json_data
    except Exception as e:
        logging.error(e)


async def generate_events_list(userdata) -> dict:
    try:
        now = datetime.datetime.now()
        today = now.strftime("%d-%m-%Y %H:%M")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Ты нейросеть, внедренная в телеграм бот (с названием Погнали, чувак).\
                    Ты настоящий знаток городов мира, особенно городов СНГ. Знаешь все их интересные места: театры, кинотеатры, исторические места и т.д. \
                    Вот тебе информация о пользователе: {userdata}\
                    Если ты незнаешь про его город или его интересы, то так и ответь, что не знаешь. попроси его дополнить данные о себе \
                    Если данные по пользователю полные, вот инструкция по ответу: отвечать на этот запрос примерно так:\
                    Поздораваться. Сказать небольшую шутку на тему телеграм-бота. Сегодня: *сегодняшняя дата*. В *городе пользователя* можно сходить в этим места, по возможности учтя его интересы, но это не обязательно\
                    1. *интересное место №1*.\
                    2. *интересноеместо №2*.\
                    3. и т.д.",
                },
                {
                    "role": "user",
                    "content": f"Куда можно сходить сегодня в моем городе: {today}",
                },
            ],
        )
        return (
            response["choices"][0]["message"]["content"],
            response["usage"]["total_tokens"],
        )
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(prompt=prompt, n=n, size=size)
        urls = []
        for i in response["data"]:
            urls.append(i["url"])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls


# async def find_user(user_id: int) -> bool:
#     '''
#     Find user in json DB
#     '''
#     json_data = json.load(open("db.json"))
#     for data in json_data:
#         if user_id == data['user_id']:
#             return True
#     return False

# async def get_user_data(user_id: int) -> dict:
#     '''
#     Find user in json DB and return data about user if exists
#     '''
#     print(f"\nGetting data for user: {user_id}...\n")
#     json_data = json.load(open("db.json"))
#     for data in json_data:
#         if type(data) is  dict:
#             if user_id == data.get('user_id'):
#                 print(f"\nGot data for user {user_id}...\n")
#                 return data
#         else:
#             print(f"Not valid data type...{type(data)}")
#     return None

# async def update_user_data(new_data: dict, user_id: int) -> bool:
#     '''
#     Find user in json DB
#     '''
#     json_data = json.load(open("db.json", encoding='utf8'))
#     print(f"\nUpdating data for user: {user_id}...\n")
#     for i, data in enumerate(json_data):
#         if type(data) is dict and type(new_data) is dict:
#             if user_id == data.get('user_id'):
#                 json_data[i].update(new_data)
#                 with open("db.json", "w", encoding='utf8') as outfile:
#                     json.dump(json_data, outfile, ensure_ascii=False)
#                 print(f'\nDict fo user {user_id} Updated!\n')
#                 return True

#     json_data.append(new_data)
#     with open("db.json", "w", encoding='utf8') as outfile:
#         json.dump(json_data, outfile, ensure_ascii=False)
#     return False

# async def add_new_user_data(user_data: dict, user_id: int) -> bool:
#     '''
#     Find user in json DB
#     '''
#     json_data = json.load(open("db.json", encoding='utf8'))

#     for i, data in enumerate(json_data):
#         if type(data) is  dict:
#             if user_id == data.get('user_id'):
#                 return None

#     json_data.append(user_data)
#     with open("db.json", "w", encoding='utf8') as outfile:
#         json.dump(json_data, outfile, ensure_ascii=False)
#     return True

# async def add_last_question(question: dict, user_id: int) -> bool:
#     '''
#     Find user in json DB
#     '''
#     json_data = json.load(open("db.json", encoding='utf8'))

#     for i, data in enumerate(json_data):
#         if type(data) is  dict:
#             if user_id == data.get('user_id'):
#                 json_data[i]['last_question'] = question
#                 with open("db.json", "w", encoding='utf8') as outfile:
#                     json.dump(json_data, outfile, ensure_ascii=False)
#                 print(f'Last question for user {user_id} Updated!')
#                 return True
