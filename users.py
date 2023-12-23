import config
import json
import psycopg2
from environs import Env
from contextlib import closing
from psycopg2.extras import DictCursor
from environs import Env


env = Env()
env.read_env()
connect_params = {
    "dbname": env("DB_NAME"),
    "user": env("DB_USER"),
    "password": env("DB_PASSWORD"),
    "host": env("DB_HOST"),
}

dict_sample = {
    "user_id": 1,
    "user_name": "Test",
    "user_firstname": "Test",
    "user_surname": "unknown",
    "age": 0,
    "sex": "unknown",
    "user_city": "unknown",
    "main_music_genres": {""},
    "techno_music_genres": {""},
    "favorite_main_music_artists": {""},
    "favorite_techno_music_artists": {""},
    "favorite_djs": {""},
    "favorite_night_clubs": {""},
    "favorite_bars": {""},
    "current_location_address": "unknown",
    "current_location_coordinates": (0, 0),
    "last_question": "unknown",
}


async def find_user(user_id: int) -> bool:
    """Find user in DB

    Args:
        user_id (int): User ID

    Returns:
        bool: True if user find in database else False
    """
    with psycopg2.connect(**connect_params) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"select exists(select from users u where user_id={user_id})"
            )
            return bool(cursor.fetchone()[0])


async def add_new_user_data(user_data: dict, user_id: int) -> bool:
    """Add new user in database

    Args:
        user_data (dict): User Data
        user_id (int): User ID

    Returns:
        bool: True if user added, False if user exist.
    """
    print(f"Creating data for user: {user_data.get('user_id')}")

    user_exist = await find_user(user_id)

    if user_exist:
        print(f"\nUser {user_id} existed\n")
        return False
    columns = ", ".join([key for key in user_data.keys()])
    values = (
        "("
        + ", ".join([str(value).replace("'", '"') for value in user_data.values()])
        + ")"
    )
    query = "INSERT INTO public.users (" + columns + ") VALUES " + values + ";"
    print("INSER query:", query)
    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                print(f"\nUser {user_id} created...\n")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    return True


async def get_user_data(user_id: int) -> dict:
    """Getting all user data

    Args:
        user_id (int): User ID

    Returns:
        dict: User data
    """

    print(f"\nGetting data for user: {user_id}...\n")
    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(f"SELECT * FROM users u WHERE user_id={user_id}")
                q = cursor.fetchone()
                if q == None:
                    print(f"No such user: {user_id}")
                    return None
                data = {
                    "user_id": q[0],
                    "user_name": q[1],
                    "user_firstname": q[2],
                    "user_surname": q[3],
                    "age": q[4],
                    "sex": q[5],
                    "user_city": q[6],
                    "main_music_genres": q[7],
                    "techno_music_genres": q[8],
                    "favorite_main_music_artists": q[9],
                    "favorite_techno_music_artists": q[10],
                    "favorite_djs": q[11],
                    "favorite_night_clubs": q[12],
                    "favorite_bars": q[13],
                    "current_location_address": q[14],
                    "current_location_coordinates": q[15],
                    "last_question": q[16],
                }
            print(f"\nGot data for user {user_id}...\n")
            print("User data:", data)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return data


async def update_user_data(new_data: dict, user_id: int) -> bool:
    """_summary_

    Args:
        new_data (dict): _description_
        user_id (int): _description_

    Returns:
        bool: _description_
    """

    # user_exist = await find_user(user_id)
    # if not user_exist:
    #     return False
    print(f"\nUpdating data for user {user_id}...\n")
    user_data = await get_user_data(user_id)
    user_data.update((k, new_data[k]) for k in set(new_data).intersection(user_data))
    col_val = [
        str(key)
        + "='"
        + str(value).replace("'", '"').replace("[", "{").replace("]", "}")
        + "'"
        for key, value in user_data.items()
        if value != None and value != "" and key != "user_id" and key != "last_question"
    ]
    print(f"\nColumn and values for update: {col_val}\n")
    query = (
        """update public.users set """
        + ", ".join(col_val)
        + " where user_id="
        + str(user_id)
    )
    print("\n Update query:", query)
    with psycopg2.connect(**connect_params) as conn:
        try:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                print(f"\nData for user {user_id} updated...\n")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    return True


async def add_last_question(question: dict, user_id: int) -> bool:
    """_summary_

    Args:
        question (dict): Last question
        user_id (int): User ID

    Returns:
        bool: True if added
    """

    with psycopg2.connect(**connect_params) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                f"""
                            UPDATE public.users
                            SET last_question=\'{question}\'
                            WHERE user_id={user_id};
                            """
            )
    print(f"Last question for user {user_id} Updated!")
    return True
