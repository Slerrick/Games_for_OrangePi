import json
import threading
from common import (
    BOT, PAYMENT_TOKEN, BUTTON_BACK, ty, dt, pl, time, 
    HELLO_TEXT, LIST_COMMANDS, FIB_TEXT
)
from My_sqlite3 import session_id_admins
from clean_DB import clear_admins, delete_inactive_accounts
import My_sqlite3 as sqlite

# Конфигурация клавиатур
KEYBOARD_MENU = ty.ReplyKeyboardMarkup(resize_keyboard=True)
KEYBOARD_MENU.row(
    ty.KeyboardButton("Категории"),
    ty.KeyboardButton("Аккаунт")
)
KEYBOARD_MENU.add(ty.KeyboardButton("Магазин SKM"))

KEYBOARD_REG = ty.InlineKeyboardMarkup()
KEYBOARD_REG.row(
    ty.InlineKeyboardButton("Войти", callback_data="enter"),
    ty.InlineKeyboardButton("Зарегистрироваться", callback_data="reg")
)
KEYBOARD_REG.add(ty.InlineKeyboardButton("Удалить аккаунт", callback_data="del"))
KEYBOARD_REG.add(ty.InlineKeyboardButton("Мои данные", callback_data="info"))

KEY_SHOP = ty.ReplyKeyboardMarkup(resize_keyboard=True)
KEY_SHOP.add(ty.KeyboardButton(
    text="Открыть веб-приложение",
    web_app=ty.WebAppInfo(url="https://slerrick.github.io/Telegram_Bot_webApp/")
))
KEY_SHOP.add(BUTTON_BACK)

KEY_CHOSEN = ty.InlineKeyboardMarkup()
KEY_CHOSEN.row(
    ty.InlineKeyboardButton("Программы", callback_data="prog"),
    ty.InlineKeyboardButton("Материалы для изучения", callback_data="learn")
)
KEY_CHOSEN.row(
    ty.InlineKeyboardButton("Железо", callback_data="hardware"),
    ty.InlineKeyboardButton("Прочее", callback_data="others")
)

# Глобальная переменная для хранения информации о платежах
payment_sessions = {}

def check_time():
    """Проверка времени для автоматических задач"""
    global session_id_admins
    while True:
        try:
            current_time = dt.now()
            if current_time.hour == 23 and current_time.minute == 39:
                clear_admins()
                delete_inactive_accounts()
                session_id_admins = [0]
                time.sleep(60)
            else:
                time.sleep(20)
        except Exception as e:
            print(f"Ошибка в фоновом потоке: {e}")
            time.sleep(60)

def check_admins(user_id: int) -> bool:
    """Проверка прав администратора"""
    return user_id in session_id_admins

def menu(message):
    """Главное меню"""
    BOT.send_message(message.chat.id, "Выберите действие:", reply_markup=KEYBOARD_MENU)

def registration(message):
    """Меню регистрации"""
    BOT.send_message(message.chat.id, "Действия с аккаунтом:", reply_markup=KEYBOARD_REG)

def send_shop_price(message):
    """Отправка магазина"""
    BOT.send_message(
        message.chat.id, 
        "Нажмите на кнопку, чтобы открыть веб-приложение", 
        reply_markup=KEY_SHOP
    )

def payment(message, amount: int):
    """Обработка платежа звездами"""
    try:
        # Сохраняем информацию о платеже для последующей обработки
        payment_sessions[message.chat.id] = {
            'amount': amount/100,
            'user_id': message.from_user.id,
            'timestamp': dt.now()
        }
        
        # Создаем инвойс для оплаты звездами
        BOT.send_invoice(
            chat_id=message.chat.id,
            title="Пополнение баланса SKM",
            description=f"Пополнение баланса на {amount} SKM",
            invoice_payload=f"skm_topup_{amount}_{message.from_user.id}",
            provider_token="",  # Токен должен поддерживать Stars
            currency="XTR",  # Код валюты для звезд Telegram
            prices=[ty.LabeledPrice(label=f"{amount} SKM", amount=payment_sessions["amount"])],  # Сумма в звездах
            photo_url="https://img.icons8.com/color/96/000000/star--v1.png",  # Иконка звезды
            photo_size=100,
            photo_width=100,
            photo_height=100,
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            is_flexible=False,
            timeout=300  # 5 минут на оплату
        )
        
    except Exception as e:
        print(f"Ошибка при создании платежа: {e}")
        BOT.send_message(message.chat.id, "Ошибка при создании платежа. Попробуйте позже.")

def send_zip_file(zip_path: str, chat_id: int):
    """Отправка ZIP файла"""
    try:
        with open(zip_path, "rb") as zip_file:
            BOT.send_document(chat_id, zip_file, caption="Вот ваш ZIP-архив!")
    except FileNotFoundError:
        BOT.send_message(chat_id, "Файл не найден. Повторите попытку позже.")
    except Exception as e:
        print(f"Ошибка при отправке файла: {e}")
        BOT.send_message(chat_id, "Ошибка при отправке файла.")

def register_user(message, additional_arg: int):
    """Регистрация пользователя"""
    name_user = message.text.strip()
    
    if len(name_user) >= 30:
        BOT.send_message(message.chat.id, "Имя слишком длинное, повторите попытку")
        return
    
    sqlite.set_user_name(name_user)
    BOT.send_message(message.chat.id, "Придумайте пароль:")
    BOT.register_next_step_handler(
        message, 
        pl(sqlite.save_info_user, additional_arg=additional_arg)
    )

# Обработчики сообщений
@BOT.message_handler(commands=["start"])
def main(message: ty.Message):
    """Обработчик команды /start"""
    BOT.send_message(
        message.chat.id, 
        f"<b>Привет, </b>{message.from_user.first_name}!{HELLO_TEXT}", 
        parse_mode="html"
    )
    menu(message)

@BOT.message_handler(commands=["web"])
def go_site(message: ty.Message):
    """Обработчик команды /web"""
    buttons_to_web = ty.InlineKeyboardMarkup()
    buttons_to_web.row(
        ty.InlineKeyboardButton("Перейти на сайт!", url="https://slerrick.github.io/WebSite3/"),
        ty.InlineKeyboardButton("На всякий случай...", callback_data="fib")
    )
    BOT.send_message(message.chat.id, "А вот и мой первый сайт 😊", reply_markup=buttons_to_web)

@BOT.message_handler(content_types=["photo", "document"])
def answer_to_file(message: ty.Message):
    """Обработчик файлов"""
    BOT.reply_to(message, "Отличный файл! Жаль, что пока я не могу работать с ним(")

@BOT.message_handler(content_types=[ty.SuccessfulPayment])
def success_payment(message: ty.Message):
    """Обработчик успешного платежа звездами"""
    try:
        # Получаем информацию о платеже
        payment_info = payment_sessions.get(message.chat.id, {})
        amount = payment_info.get('amount', 0)
        user_id = payment_info.get('user_id', message.from_user.id)
        
        # Если информация не найдена в сессии, пытаемся извлечь из payload
        if amount == 0:
            payload = message.successful_payment.invoice_payload
            if payload and payload.startswith('skm_topup_'):
                parts = payload.split('_')
                if len(parts) >= 3:
                    amount = int(parts[2])
        
        # Зачисляем средства на счет пользователя
        if amount > 0:
            sqlite.set_skm_user(message, amount, user_id)
            BOT.send_message(
                message.chat.id, 
                f"✅ Оплата прошла успешно! На ваш счет зачислено {amount} SKM."
            )
            
            # Очищаем сессию платежа
            if message.chat.id in payment_sessions:
                del payment_sessions[message.chat.id]
                
        else:
            BOT.send_message(
                message.chat.id, 
                "❌ Не удалось обработать платеж. Обратитесь к администратору."
            )
            
    except Exception as e:
        print(f"Ошибка при обработке платежа: {e}")
        BOT.send_message(
            message.chat.id, 
            "❌ Произошла ошибка при обработке платежа. Обратитесь к администратору."
        )

@BOT.message_handler(content_types=["web_app_data"])
def handle_web_app_data(message: ty.Message):
    """Обработчик данных из веб-приложения"""
    try:
        res = json.loads(message.web_app_data.data)
        amount = res.get('amount', 0)
        
        if amount > 0:
            # Создаем клавиатуру для подтверждения оплаты
            key_confirm_payment = ty.InlineKeyboardMarkup()
            key_confirm_payment.row(
                ty.InlineKeyboardButton(f"Оплатить {amount} звезд", callback_data=f"pay_{amount}"),
                ty.InlineKeyboardButton("Отмена", callback_data="cancel_payment")
            )
            
            BOT.send_message(
                message.chat.id, 
                f"Для пополнения баланса на {amount} SKM нажмите кнопку оплаты:", 
                reply_markup=key_confirm_payment
            )
        else:
            BOT.send_message(message.chat.id, "Неверная сумма для пополнения.")
            
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        BOT.send_message(message.chat.id, "Ошибка обработки данных")
    except Exception as e:
        print(f"Ошибка обработки web app данных: {e}")
        BOT.send_message(message.chat.id, "Произошла ошибка")

@BOT.message_handler(commands=["admin"])
def admin_command(message: ty.Message):
    """Обработчик команды /admin"""
    if check_admins(message.from_user.id):
        try:
            BOT.send_message(message.chat.id, "Дарова!")
            BOT.send_message(message.chat.id, LIST_COMMANDS)
            print("Предоставлены права админа")
        except Exception as e:
            print(f"Ошибка в команде /admin: {e}")
    else:
        BOT.send_message(message.chat.id, "Не админ!")

@BOT.message_handler(commands=["admin_list"])
def get_admin_list_command(message: ty.Message):
    """Обработчик команды /admin_list"""
    if check_admins(message.from_user.id):
        BOT.send_message(message.chat.id, sqlite.list_admins())

@BOT.message_handler(commands=["user_list"])
def get_user_list_command(message: ty.Message):
    """Обработчик команды /user_list"""
    if check_admins(message.from_user.id):
        BOT.send_message(message.chat.id, sqlite.list_users())

@BOT.message_handler(content_types=["text"])
def handle_text(message: ty.Message):
    """Обработчик текстовых сообщений"""
    text = message.text.strip()
    
    if text == "Получить файл":
        BOT.send_message(message.chat.id, "Подождите...")
        send_zip_file("./javascript-snakes-master.zip", message.chat.id)
    elif text == "Аккаунт":
        registration(message)
    elif text == "Назад":
        menu(message)
    elif text == "Магазин SKM":
        send_shop_price(message)
    elif text == "Категории":
        BOT.send_message(message.chat.id, "Ссылки на страницы тем", reply_markup=KEY_CHOSEN)

@BOT.callback_query_handler(func=lambda call: True)
def handle_callback(call: ty.CallbackQuery):
    """Обработчик callback запросов"""
    message = call.message
    user_id = message.from_user.id
    
    try:
        if call.data == "fib":
            BOT.send_message(message.chat.id, FIB_TEXT)
            BOT.answer_callback_query(call.id, text="Запрос принят.")
        
        elif call.data == "reg":
            if sqlite.reg_user_first_check(message):
                BOT.send_message(
                    message.chat.id, 
                    "Вы уже зарегистрированы. Если не можете войти в аккаунт, его можно удалить и создать новый."
                )
            else:
                BOT.send_message(message.chat.id, "Введите имя пользователя:")
                BOT.register_next_step_handler(
                    message, 
                    pl(register_user, additional_arg=user_id)
                )
            BOT.answer_callback_query(call.id, text="Запрос принят.")
        
        elif call.data == "enter":
            BOT.send_message(message.chat.id, "Введи одним сообщением имя, а потом через пробел пароль.")
            BOT.register_next_step_handler(
                message, 
                pl(sqlite.enter_user, additional_arg=user_id)
            )
            BOT.answer_callback_query(call.id, text="Запрос принят.")
        
        elif call.data == "del":
            BOT.send_message(message.chat.id, "Напишите ДА/НЕТ, если хотите удалить/оставить аккаунт.")
            BOT.register_next_step_handler(
                message, 
                pl(sqlite.delete_account, additional_arg=user_id)
            )
            BOT.answer_callback_query(call.id, text="Запрос принят.")
        
        elif call.data == "info":
            user_info = sqlite.create_table(message, user_id)
            BOT.send_message(message.chat.id, user_info, parse_mode="html")
            BOT.answer_callback_query(call.id)
        
        elif call.data.startswith("pay_"):
            # Обработка запроса на оплату
            try:
                amount = int(call.data.split("_")[1])
                payment(message, amount)
            except (ValueError, IndexError):
                BOT.send_message(message.chat.id, "Ошибка обработки платежа.")
            BOT.answer_callback_query(call.id)
        
        elif call.data == "cancel_payment":
            BOT.send_message(message.chat.id, "Оплата отменена.")
            BOT.answer_callback_query(call.id)
        
        elif call.data in ["5200", "8000", "10000", "15000"]:
            # Прямой вызов оплаты для старых callback'ов
            payment(message, int(call.data))
            BOT.answer_callback_query(call.id)
            
    except Exception as e:
        print(f"Ошибка обработки callback: {e}")
        BOT.answer_callback_query(call.id, text="Произошла ошибка")

# Функция для очистки устаревших платежных сессий
def cleanup_payment_sessions():
    """Очистка устаревших платежных сессий"""
    while True:
        try:
            current_time = dt.now()
            expired_sessions = []
            
            for chat_id, session_data in payment_sessions.items():
                if (current_time - session_data['timestamp']).total_seconds() > 3600:  # 1 час
                    expired_sessions.append(chat_id)
            
            for chat_id in expired_sessions:
                del payment_sessions[chat_id]
                
            time.sleep(3600)  # Проверка каждый час
            
        except Exception as e:
            print(f"Ошибка при очистке платежных сессий: {e}")
            time.sleep(600)

# Запуск приложения
if __name__ == "__main__":
    # Запуск фоновых задач
    background_thread = threading.Thread(target=check_time, daemon=True)
    background_thread.start()
    
    # Запуск очистки платежных сессий
    cleanup_thread = threading.Thread(target=cleanup_payment_sessions, daemon=True)
    cleanup_thread.start()
    
    print("Бот запущен...")
    BOT.polling(non_stop=True, interval=3)