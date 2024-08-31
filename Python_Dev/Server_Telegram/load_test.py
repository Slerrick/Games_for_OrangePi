import asyncio
import aiohttp
import random
import threading
import time
from   datetime              import    datetime       as    dt
import Info_sys

BOT_TOKEN = '7399585156:AAHZ1p219hn2agQ79qbULlcOwNtqTzCeJu4'  # Замените своим токеном
CHAT_ID = '5155181543'  # Замените на ID чата или пользователя

# Пример сообщении, которые будут отправлены
messages = [
    "Аккаунт",
    "/admin",
    "Магазин",
    "Получить файл",
    "Тестовое сообщение."
]

async def send_message(session, message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
    }
    async with session.post(url, json=data) as response:
        return await response.json()

async def load_test(num_users):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_users):
            message = random.choice(messages)
            tasks.append(send_message(session, message))
        responses = await asyncio.gather(*tasks)
        return responses

if __name__ == '__main__':
    num_users = 100  # Количество имитируемых пользователей
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(load_test(num_users))

    for response in responses:
        print(response)
def check_time():
  global session_id_admins
  while True: 
    Info_sys.check_cpu()
    Info_sys.check_disk()
    session_id_admins = [0]
    time.sleep(0.5)

threading.Thread(target=check_time).start()