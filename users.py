import config
import json
import psycopg2
from environs import Env
from contextlib import closing
from psycopg2.extras import DictCursor
from environs import Env
env = Env()
env.read_env()
connect_params = {'dbname':env('DB_NAME'),
           'user':env('DB_USER'),
           'password':env('DB_PASSWORD'),
           'host':env('DB_HOST')}


async def find_user(user_id: int) -> bool:
    """Find user in json DB

    Args:
        user_id (int): User ID

    Returns:
        bool: True if user find in database else False
    """
    with psycopg2.connect(**connect_params) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(f'select exists(select from users u where user_id={user_id})')
            return bool(cursor.fetchone()[0])


async def add_new_user_data(user_data: dict, user_id: int) -> bool:
    """Add new user in database

    Args:
        user_data (dict): User Data
        user_id (int): User ID

    Returns:
        bool: True if user added, False if user exist.
    """
 
    user_name = user_data.get('user_name')
    user_firstname = user_data.get('user_firstname')
    user_surname = user_data.get('user_surname')
    age = user_data.get('age')
    sex = user_data.get('sex')
    user_city = user_data.get('user_city')
    last_question = user_data.get('last_question')
    misc_data = json.dumps(user_data.get('misc_data'))

    user_exist = await find_user(user_id)
    if user_exist:
        return False
    
    with psycopg2.connect(**connect_params) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(f"""
                           INSERT INTO public.users (user_id,user_name,user_firstname,user_surname,age,sex,user_city,last_question,misc_data)
                           VALUES ({user_id},\'{user_name}\',\'{user_firstname}\',\'{user_surname}\',
                           {age},{sex},\'{user_city}\',\'{last_question}\',\'{misc_data}\');
                           """)
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
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(f'SELECT * FROM users u WHERE user_id={user_id}')
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
                "last_question": q[7],
                "misc_data": q[8],
            }    
        print(f"\nGot data for user {user_id}...\n")
        return data


async def update_user_data(new_data: dict, user_id: int) -> bool:
    """_summary_

    Args:
        new_data (dict): _description_
        user_id (int): _description_

    Returns:
        bool: _description_
    """
        
    user_exist = await find_user(user_id)
    if not user_exist:
        return False
    
    columns = new_data.keys()
    values = [new_data[column] for column in columns]
    
    with psycopg2.connect(**connect_params) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('INSERT INTO public.users (%s) VALUES %s')
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
            cursor.execute(f"""
                            UPDATE public.users
                            SET last_question=\'{question}\'
                            WHERE user_id={user_id};
                            """)
    print(f'Last question for user {user_id} Updated!')
    return True
