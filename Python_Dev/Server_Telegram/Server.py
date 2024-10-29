######################
import Info_sys
import My_sqlite3     as        sql3
from   common         import    BOT, PAYMENT_TOKEN, BUTTON_BACK, ty, dt, pl, time
#File common is private, create his.
from   My_sqlite3     import    session_id_admins
from   clean_DB       import    clear_admins, delete_inactive_accounts
######################
import threading
import json 



#Function and variables without use telebot:
def check_time():
  global session_id_admins
  while True:
    if dt.now().hour == 23 and dt.now().minute == 39: 
        clear_admins()
        delete_inactive_accounts()
        session_id_admins = [0]
        time.sleep(60)
    else:
        time.sleep(20)
def check_admins(id):
    if id in session_id_admins:
        return True
    else:
        return False
    #RUN IN THE END OF PROGRAM
HELLO_TEXT = """
Твой единомышленник в мире программирования!
Этот бот постарается помочь разобраться начальном освоении программирования   :) 
•📚Полезные статьи: Изучай статьи на актуальные темы (Type/Java Script; Python).
•💡Проекты: Узнай о проектах и почерпни вдохновение для собственных, помогай решать проблемы и исправляй свои!
•🛒Магазин: Покупай SKM для внутренних товаров..."""
FIB_TEXT = """import timeit
def fibonacci_iterative(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return 0

# Измеряем время выполнения итеративной функции
elapsed_time_iterative = timeit.timeit(lambda: fibonacci_iterative(1_500_000), number=1)
print(f"Время выполнения: {elapsed_time_iterative:.2f} секунд")
f = input()

Скопируй код и проверь, за какое время твой пк сможет пересчитать по порядку полторамиллиона раз последовательность Фибоначчи!"""
LIST_COMMANDS = """
Вот список команд:
1) /user_list
2) /admin_list"""
#MULTI_FUNCTION

#MENU AND IT'S MODULES

################################
KEY_MENU = ty.ReplyKeyboardMarkup(resize_keyboard=True) 
button_file = ty.KeyboardButton("Категории")
button_login = ty.KeyboardButton("Аккаунт")
button_enter = ty.KeyboardButton("Магазин")
KEY_MENU.row(button_file, button_login)
KEY_MENU.add(button_enter)
###############################
def Menu(message):
    BOT.send_message(message.chat.id, "Выберите действие:", reply_markup=KEY_MENU)
################################
KEY_REG = ty.InlineKeyboardMarkup() 
button_deleted = ty.InlineKeyboardButton("Удалить аккаунт", callback_data="del")
button_state = ty.InlineKeyboardButton("Мои данные", callback_data="info")
button_login = ty.InlineKeyboardButton("Зарегистрироваться", callback_data="reg")
button_enter = ty.InlineKeyboardButton("Войти", callback_data="enter")
KEY_REG.row(button_enter, button_login)
KEY_REG.add(button_deleted)
KEY_REG.add(button_state)
################################
def Registration(message): 
    BOT.send_message(message.chat.id, "Действия с аккаунтом:", reply_markup=KEY_REG)
################################
KEY_SHOP = ty.ReplyKeyboardMarkup(resize_keyboard=True)
button = ty.KeyboardButton(
text="Открыть веб-приложение", web_app=ty.WebAppInfo(url="https://slerrick.github.io/Telegram_Bot_webApp/"))
KEY_SHOP.add(button)
KEY_SHOP.add(BUTTON_BACK)
################################
def send_shop_price(message):
    BOT.send_message(message.chat.id, "Нажмите на кнопку, чтобы открыть веб-приложение(10 секунд):", reply_markup=KEY_SHOP)
################################
KEY_CHOSEN = ty.ReplyKeyboardMarkup(resize_keyboard=True)
button_programm = ty.KeyboardButton("Программы")
button_learn = ty.KeyboardButton("Материалы для изучения")
button_hard = ty.KeyboardButton("Железо")
button_other = ty.KeyboardButton("Прочее")
KEY_CHOSEN.row(button_programm, button_learn)
KEY_CHOSEN.row(button_hard, button_other)
KEY_CHOSEN.add(BUTTON_BACK)
def payment(message):
    BOT.send_invoice(
        message.chat.id,
        title="SK_MONEYS",
        description="I'm rich",
        invoice_payload="invoice",
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=[ty.LabeledPrice("Название товара", 10000)],
        timeout=10)



#SEND FILES
def send_zip_file(zip_path: str, chat_id: int):
    try:
        with open(zip_path, "rb") as zip_file:
            BOT.send_document(chat_id, zip_file, caption="Вот ваш ZIP-архив!")
    except FileNotFoundError:
        BOT.send_message(chat_id, "Файл не найден. Повторите попытку позже.")



#LOGIN
def register_user(message, additional_arg):
    name_user = message.text
    sql3.Set_user_name(name_user)
    if len(name_user) >= 30:
        BOT.send_message(message.chat.id, "Имя слишком длинное, повторите попытку")
        return 0
    BOT.send_message(message.chat.id, "Придумайте пароль:")
    BOT.register_next_step_handler(message, pl(sql3.save_info_user, additional_arg=additional_arg))
    Info_sys.check_disk()



#Basic functions
@BOT.message_handler(commands=["start"])
def Main(message: ty.Message):
    BOT.send_message(message.chat.id, f"<b>Привет, </b>{message.from_user.first_name}!{HELLO_TEXT}", parse_mode="html")
    Menu(message)

@BOT.message_handler(commands=["web"])
def Go_site(message: ty.Message):
    Buttons_to_web = ty.InlineKeyboardMarkup()
    Btn_web1 = ty.InlineKeyboardButton("Перейти на сайт!", url="https://slerrick.github.io/WebSite3/")
    Btn_web2 = ty.InlineKeyboardButton("На всякий случай...", callback_data="fib")  
    Buttons_to_web.row(Btn_web1, Btn_web2)
    BOT.send_message(message.chat.id, "А вот и мой первый сайт 😊", reply_markup=Buttons_to_web)

@BOT.message_handler(content_types=["photo", "file"])
def Answer_to_file(chatick: ty.Message):
    BOT.reply_to(chatick, "Отличный файл! Жаль, что пока я не могу работать с ним(")
####################################
@BOT.message_handler(content_types=[ty.SuccessfulPayment])
def Success(message: ty.Message):
    BOT.send_message(message.chat.id, f"Success: {message.successful_payment.order_info}")
@BOT.message_handler(content_types=["web_app_data"])
def json_web(message: ty.Message):
    res = json.loads(message.web_app_data.data)
    KEY_GET_SKM = ty.InlineKeyboardMarkup()
    button_money = ty.InlineKeyboardButton("Получить на счет", callback_data=str(res['amount']))
    KEY_GET_SKM.add(button_money)
    BOT.send_message(message.chat.id, f"Пополнение баланса на {res['amount']}", reply_markup=KEY_GET_SKM)
####################################
@BOT.message_handler(commands=["admin"])
def Admin(message: ty.Message):
    if check_admins(message.from_user.id):
        try:
            BOT.send_message(message.chat.id, "Дарова!")
            BOT.send_message(message.chat.id, LIST_COMMANDS)
            print("Предоставлены права админа")
            Info_sys.check_cpu()
            return 0
        except Exception as e:
            print(e)    
    BOT.send_message(message.chat.id, "Не админ!")      

@BOT.message_handler(commands=["admin_list"])
def get_admin_list(message: ty.Message):
    if check_admins(message.from_user.id):
        BOT.send_message(message.chat.id, sql3.List_admins())

@BOT.message_handler(commands=["user_list"])
def get_user_list(message):
    if check_admins(message.from_user.id):
        BOT.send_message(message.chat.id, sql3.List_users())

@BOT.message_handler(content_types=["text"])
def on_click(message: ty.Message):
    if message.text == "Получить файл":
        BOT.send_message(message.chat.id, "Подождите...")
        send_zip_file("./javascript-snakes-master.zip", message.chat.id)
    elif message.text == "Аккаунт":
        Registration(message)
    elif message.text == "Назад":
        Menu(message)
    elif message.text == "Магазин":
        send_shop_price(message)
    elif message.text == "Категории":
        BOT.send_message(message.chat.id, "👾", reply_markup=KEY_CHOSEN)



@BOT.callback_query_handler(func=lambda call: True or call)
def Call_BOT(call: ty.CallbackQuery):
    messages = call.message
    user_id = messages.from_user.id
    if call.data == "fib":
        BOT.send_message(call.message.chat.id, FIB_TEXT)
        BOT.answer_callback_query(call.id)
        BOT.answer_callback_query(call.id, text="Запрос принят.")
    if call.data == "reg":
        if sql3.Reg_user_first_check(call.message):
            BOT.send_message(call.message.chat.id, "Вы уже зарегистрированы. Если не можете войти в аккаунт, его можно удалить и создать новый.")
            BOT.answer_callback_query(call.id, text="Запрос принят.")
            return 0
        BOT.send_message(call.message.chat.id, "Введите имя пользователя:")
        BOT.register_next_step_handler(messages, pl(register_user, additional_arg=user_id))
        BOT.answer_callback_query(call.id, text="Запрос принят.")
    if call.data == "enter":
        BOT.send_message(messages.chat.id, "Введи одним сообщением имя, а потом через пробел пароль.")
        BOT.register_next_step_handler(messages, pl(sql3.Enter_user, additional_arg=user_id))
        BOT.answer_callback_query(call.id, text="Запрос принят.")
    if call.data == "del":
        BOT.send_message(call.message.chat.id, "Напишите ДА/НЕТ, если хотите удалить/оставить аккаунт.")
        BOT.register_next_step_handler(call.message, pl(sql3.delete_account, additional_arg=user_id))
        BOT.answer_callback_query(call.id, text="Запрос принят.")
    if call.data == "info":
        BOT.send_message(messages.chat.id, sql3.create_table(messages, user_id), parse_mode="html")
        BOT.answer_callback_query(call.id)
    if call.data in ["5200", "8000", "10000", "15000"]:
        sql3.set_skm_user(messages, int(call.data), user_id)

#END_PROGRAM
threading.Thread(target=check_time).start()
BOT.polling(non_stop=True, interval=3)