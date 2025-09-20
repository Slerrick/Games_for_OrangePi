import asyncio
import aiohttp
import random
import threading
import Info_sys
from common import time, BOT_TOKEN
from typing import List, Dict, Any

CHAT_ID = '5155181543'

messages = [
    "Аккаунт",
    "/admin",
    "Магазин",
    "Получить файл",
    "Тестовое сообщение."
]

async def send_message(session: aiohttp.ClientSession, message: str) -> Dict[str, Any]:
    """Отправка сообщения через Telegram API"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
    }
    
    try:
        async with session.post(url, json=data, timeout=10) as response:
            return await response.json()
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
        return {'error': str(e)}

async def load_test(num_users: int) -> List[Dict[str, Any]]:
    """Нагрузочное тестирование"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_users):
            message = random.choice(messages)
            tasks.append(send_message(session, message))
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

def check_time():
    """Проверка системных метрик в отдельном потоке"""
    global session_id_admins
    while True:
        try:
            Info_sys.check_cpu()
            Info_sys.check_disk()
            session_id_admins = [0]
            time.sleep(30)  # Увеличил интервал для снижения нагрузки
        except Exception as e:
            print(f"Ошибка в потоке мониторинга: {e}")
            time.sleep(60)

def run_load_test():
    """Запуск нагрузочного тестирования"""
    num_users = 100
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        responses = loop.run_until_complete(load_test(num_users))
        
        success_count = 0
        for response in responses:
            if isinstance(response, dict) and response.get('ok'):
                success_count += 1
            else:
                print(f"Ошибка ответа: {response}")
        
        print(f"Успешно отправлено: {success_count}/{num_users}")
        
    except Exception as e:
        print(f"Ошибка при нагрузочном тестировании: {e}")
    finally:
        if 'loop' in locals():
            loop.close()

if __name__ == '__main__':
    # Запуск мониторинга в отдельном потоке
    monitor_thread = threading.Thread(target=check_time, daemon=True)
    monitor_thread.start()
    
    # Запуск нагрузочного теста
    run_load_test()