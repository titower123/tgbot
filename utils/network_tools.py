import enum
import logging

import aiohttp
from datetime import datetime, timedelta
import threading
import requests
from core.config import BASE_URL_AI, BASE_URL_SERVER, admins, moderators, operators, LOGIN, PASSWORD


class HttpMethod(enum.Enum):
    get = 0
    post = 1
    put = 2
    delete = 3


TOKEN = ''

timer = ''


async def get_users():
    logging.info("Загрузка пользователей...")
    result = await send_request("/users", HttpMethod.get, True)
    if result[0] == 200:
        users = result[1]
        for user in users:
            match user["role"]:
                case 3:
                    admins.append(user["user_id"])
                case 2:
                    moderators.append(user["user_id"])
                case 1:
                    operators.append(user["user_id"])
        logging.info("Загрузка пользователей завершена успешно!")
    else:
        logging.error(f"{result[0]}|{result[1]}")


def get_token():
    logging.info("Получаю токен")
    r = requests.post(BASE_URL_SERVER + f'/auth/token?username={LOGIN}&password={PASSWORD}')
    global TOKEN
    try:
        TOKEN = r.json()['access_token']
        expired_time = r.json()['expired_time']
        logging.info("Токен получен")
        logging.info(f"Обновление токена через {expired_time} минут")
        autoupdate_token(expired_time)
    except Exception as e:
        logging.error(e)


def autoupdate_token(expired_time):
    run_at = datetime.now() + timedelta(minutes=expired_time)
    delay = (run_at - datetime.now()).total_seconds()
    global timer
    timer = threading.Timer(delay, get_token)
    timer.start()
    logging.info("Таймер запущен")


def stop_timer():
    global timer
    timer.cancel()


async def send_request_to_ai(json):
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL_AI + '/model', json=json) as resp:
            response = await resp.json()
            return response


async def send_request(path: str, method: HttpMethod, auth: bool, json=None):
    async with aiohttp.ClientSession() as session:
        match method:
            case HttpMethod.post:
                async with session.post(BASE_URL_SERVER + path,
                                        headers={'Authorization': f'Bearer {TOKEN}',
                                                 'Content-Type': 'application/json'} if auth
                                        else None,
                                        json=json if json is not None else None) as resp:
                    return resp.status, await resp.json()
            case HttpMethod.get:
                async with session.get(BASE_URL_SERVER + path,
                                       headers={'Authorization': f'Bearer {TOKEN}',
                                                'Content-Type': 'application/json'} if auth
                                       else None,
                                       json=json if json is not None else None) as resp:  # [1]
                    return resp.status, await resp.json()
            case HttpMethod.put:
                async with session.put(BASE_URL_SERVER + path,
                                       headers={'Authorization': f'Bearer {TOKEN}',
                                                'Content-Type': 'application/json'} if auth
                                       else None,
                                       json=json if json is not None else None) as resp:  # [1]
                    return resp.status, await resp.json()
            case HttpMethod.delete:
                async with session.delete(BASE_URL_SERVER + path,
                                          headers={'Authorization': f'Bearer {TOKEN}',
                                                   'Content-Type': 'application/json'} if auth
                                          else None,
                                          json=json if json is not None else None) as resp:  # [1]
                    return resp.status, await resp.json()
