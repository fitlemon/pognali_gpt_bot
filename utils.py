import openai
import logging
import datetime
import json
from pprint import pprint
from environs import Env
import psycopg2
from psycopg2.extras import DictCursor
from sentence_transformers import SentenceTransformer, util


# import env config file
env = Env()
env.read_env()
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

## tags weight
TAGS_WEIGHT = 0.7
DESC_WEIGHT = 0.3


## Rangeer events by sementics compatibility
async def rangeer(events_text, user_text, count=5):
    print("\n\n\nScoring rangeer between:")
    print("\nUser context:", user_text)
    print("\nEvents/venues context:", events_text)
    print("\n\n\n")
    embedding_user = model.encode(user_text, convert_to_tensor=True)
    cosine_scores = []
    for id, text in events_text:
        if text == "":
            continue
        embedding_event = model.encode(str(text), convert_to_tensor=True)
        # compute similarity scores of two embeddings
        cosine_score = util.pytorch_cos_sim(embedding_user, embedding_event)
        cosine_scores.append([id, text, cosine_score])
    # print(sorted(cosine_scores, reverse=True, key=lambda x: x[2]))
    best_cosine_scores = sorted(cosine_scores, reverse=True, key=lambda x: x[2])[:count]
    print(best_cosine_scores)
    return best_cosine_scores


## Rangeer events by sementics compatibility in tags and desc
async def rangeer_by_two(events_text, user_text, count=5):
    print("\n\n\nScoring rangeer between:")
    print("\nUser context:", user_text)
    print("\nEvents context:", events_text)
    print("\n\n\n")
    embedding_user = model.encode(user_text, convert_to_tensor=True)
    cosine_scores = []
    for id, desc, tag in events_text:
        if desc == "" or tag == "":
            continue
        # compute similarity scores of two embeddings tags and user text
        embedding_tag = model.encode(str(tag), convert_to_tensor=True)
        cosine_score_tag = util.pytorch_cos_sim(embedding_user, embedding_tag)
        # compute similarity scores of two embeddings desc and user text
        embedding_desc = model.encode(str(desc), convert_to_tensor=True)
        cosine_score_desc = util.pytorch_cos_sim(embedding_user, embedding_desc)
        cosine_score = TAGS_WEIGHT * cosine_score_tag + DESC_WEIGHT * cosine_score_desc
        cosine_scores.append([id, cosine_score])
    # print(sorted(cosine_scores, reverse=True, key=lambda x: x[2]))
    best_cosine_scores = sorted(cosine_scores, reverse=True, key=lambda x: x[1])[:count]
    print(best_cosine_scores)
    return best_cosine_scores


openai.api_key = env("OPENAI_TOKEN")
max_token_count = 4096
logging.basicConfig(
    filename="logging.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

connect_params = {
    "dbname": env("DB_NAME"),
    "user": env("DB_USER"),
    "password": env("DB_PASSWORD"),
    "host": env("DB_HOST"),
}

current_date = "2023-09-01"  # For test imitate now date


async def prompt_to_dude(prompt, userdata) -> dict:
    try:
        last_question = userdata["last_question"]
        del userdata["last_question"]
        intro_rule = "Не здаровайся. Ты мой друг (бро)!! Я твой лучший друг (бро)!! Ты берешь у меня интервью уже пол часа. Ты задаешь мне вопросы, я на них отвечаю. Ты должен узнать какие ночные клубы, мероприятия мне нравятся. Какой жанр музыки, особенно в техно направлении, мне нравится"
        question = f"Вот твой последний вопрос:  {last_question} \n"
        user_message = f"\n Вот мой ответ на этот вопрос:  {prompt}. \n"
        user_dict = f"Также я тебе дам  Python словарь, где приведена информация которой ты обладаешь обо мне на текущий момент.:  \n \
                   ```{userdata}```\n"
        final_rule = "не здаровайся. Твои следующие действия: \n1) начни разговор с шутки про ИИ или тусоки (Don't  greet me). 2) Задавай уточняющий вопрос чтобы заполнить информацию обо мне (например, мой возраст, пол, мои любимые музыкальные жанры, техно жанры, любимые техно-артисты, любимые ночные клубы, бары, тусовки).  \n  \n P.S.: Добавляй emojies в свой текст"
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
                response["choices"][0]["message"]["content"]
                .replace("'", '"')
                .replace("`", "")
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


# Get 6 randon tags from DB
# #  SELECT *
#   FROM data_set
#   ORDER BY random()
#   LIMIT 6;
async def get_random_genres():
    """
    get Random 6 tags to show
    """
    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(f"SELECT name, slug FROM tags ORDER BY random() LIMIT 6")
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                    return None
                tags = q
            print(tags)
            print(f"\nGot tags...\n")
            print("Random tags are:", tags)
            return tags
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# Get upcoming events by date
async def get_upcoming_events_by_col(col: str) -> list:
    """_summary_

    Args:
        col (str): name of column to return

    Returns:
        list: [id, column]
    """

    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    f"SELECT id, {col} FROM events WHERE start_date > '{current_date}'"
                )
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                data = q
            print(f"\nGot {len(data)} events...\n")
            data = [
                [x, y.replace("<br>", "\n").replace("<p>", "").replace("</p>", "")]
                for x, y in data
            ]
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# Get upcoming events by date
async def get_upcoming_events_desc_tags() -> list:
    """_summary_

    Returns:
        list: [id, desc, tags]
    """

    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT events.id, description , CONCAT(STRING_AGG(name, ', '), ', ', STRING_AGG(name_rus, ', ')) as event_tags FROM events LEFT JOIN taggable ON events.id = taggable.taggable_id LEFT JOIN tags on taggable.tag_id = tags.id WHERE taggable_type like '%Event%' and events.start_date > '{current_date}' GROUP By events.id;"
                cursor.execute(query)
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                data = q
            print(f"\nGot {len(data)} events...\n")
            data = [
                [x, y.replace("<br>", "\n").replace("<p>", "").replace("</p>", ""), z]
                for x, y, z in data
            ]
            return data

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# Get upcoming events by id
async def get_upcoming_events_by_id(ids: tuple, columns: list) -> list:
    """_summary_

    Args:
        ids (tuple): Tuple of ids that need to return
        idcolumns (list): List of columns to select

    Returns:
        list: [id, *column]
    """

    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT id, {', '.join(columns)} FROM events WHERE id in {ids}"
                print(query)
                cursor.execute(query)
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                    return None
                data = q
            print(f"\nGot {len(data)} events...\n")
            print("Events are:", data)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# Get upcoming events by tag
async def get_events_tags() -> list:
    """_summary_

    Args:
        ids (tuple): Tuple of ids that need to return

    Returns:
        list: [id, *column]
    """

    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT events.id, title, CONCAT(STRING_AGG(name, ', '), ', ', STRING_AGG(name_rus, ', ')) as tags FROM events INNER JOIN taggable ON events.id = taggable.taggable_id LEFT JOIN tags on taggable.tag_id = tags.id WHERE taggable_type like '%Event%' and events.start_date > '{current_date}' GROUP By events.id;  "
                print(query)
                cursor.execute(query)
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                    return None
                data = q
            print(f"\nGot {len(data)} events...\n")
            print("Events are:", data)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# Get upcoming events by tag
async def get_upcoming_events_ids_by_tag(tag: str) -> list:
    """_summary_

    Args:
        ids (tuple): Tuple of ids that need to return

    Returns:
        list: (ids)
    """

    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT events.id FROM events INNER JOIN taggable ON events.id = taggable.taggable_id LEFT JOIN tags on taggable.tag_id = tags.id WHERE taggable_type like '%Event%' and events.start_date > '{current_date}' and tags.slug like '%{tag}%' GROUP By events.id; "
                print(query)
                cursor.execute(query)
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                    return None
                data = q
            print(f"\nGot {len(data)} events...\n")
            print("Events are:", data)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# Get upcoming events (with tags) by id
async def get_upcoming_events_with_tags_by_id(ids: tuple, columns: list) -> list:
    """Return list of events by given ids

    Args:
        ids (tuple): fiven list of id
        columns (list): which columns should extract

    Returns:
        list: list of events
    """
    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT events.id, {', '.join(columns)}, CONCAT(STRING_AGG(name, ', '), ', ', STRING_AGG(name_rus, ', ')) as event_tags FROM events LEFT JOIN taggable ON events.id = taggable.taggable_id LEFT JOIN tags on taggable.tag_id = tags.id WHERE taggable_type like '%Event%' and events.start_date > '{current_date}' and events.id in {str(ids).replace('[', '(').replace(']', ')')} GROUP By events.id;"
                print(query)
                cursor.execute(query)
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                data = q
            print(f"\nGot {len(data)} events...\n")
            print("Events are:", data)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    return None


# Get upcoming events (with tags)
async def get_upcoming_events_with_tags(columns: list) -> list:
    """Return list of events by given ids

    Args:
        ids (tuple): fiven list of id
        columns (list): which columns should extract

    Returns:
        list: list of events
    """
    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                query = f"SELECT events.id, {columns}, CONCAT(STRING_AGG(name, ', '), ', ', STRING_AGG(name_rus, ', ')) as event_tags FROM events LEFT JOIN taggable ON events.id = taggable.taggable_id LEFT JOIN tags on taggable.tag_id = tags.id WHERE taggable_type like '%Event%' and events.start_date > '{current_date}' GROUP By events.id;"
                print(query)
                cursor.execute(query)
                q = cursor.fetchall()
                if q == None:
                    print(f"Tags weren't found")
                data = q
            print(f"\nGot {len(data)} events...\n")
            print("Events are:", data)
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    return None
