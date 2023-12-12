import openai
import logging
import config
import datetime

openai.api_key = config.OPENAI_TOKEN



async def generate_text(prompt, userdata) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
                    f"Ты нейросеть, внедренная в телеграм боат- гид ассистента по интересным местам и мероприятиям города. \
                    Ты настоящий знаток города Москвы. Знаешь все его интересные места: театры, кинотеатры, исторические места и т.д. \
                    Вот тебе информация о пользователе: {userdata}\
                    В данном режиме пользователь тебе отправляет свободное сообщение. \
                        Ответ на его запрос коротко и напомни ему, что твоя задача поиск интересных мест \
                            и не предназначен на раскрытые ответы на его свободные запросы\
                    "},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)
 
async def generate_events_list(userdata) -> dict:
    try:
        now = datetime.datetime.now()
        today = now.strftime("%d-%m-%Y %H:%M")
        my_city = 'Москва'
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                 {"role": "system", "content": 
                    f"Ты нейросеть, внедренная в телеграм бот- гид ассистента по интересным местам и мероприятиям города. \
                    Ты настоящий знаток городов мира, особенно городов СНГ. Знаешь все их интересные места: театры, кинотеатры, исторические места и т.д. \
                    Вот тебе информация о пользователе: {userdata}\
                    Инструкция по ответу: отвечать на этот запрос примерно так:\
                    Поздораваться. Сказать небольшую шутку. Сегодня: *сегодняшняя дата*. В *городе пользователя* можно сходить в этим места, по возможности учтя его интересы, но это не обязательно\
                    1. *интересное место №1*.\
                    2. *интересноеместо №2*.\
                    3. и т.д.\
                    Если ты незнаешь про его город, то так и ответь, что не знаешь. \
                    Также если данные пользователя отсутствует, например, город: unknown, а интересы также пусты, деликатно предложи заполнить данные\
                    "},
                {"role": "user", "content": f"Куда можно сходить сегодня в моем городе сегодня: {today}"}
            ]
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)
        
           
async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            prompt=prompt,
            n=n,
            size=size
        )
        urls = []
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls