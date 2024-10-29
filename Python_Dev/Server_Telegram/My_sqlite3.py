import      sqlite3        as sqlite
import      hashlib        as hash
import      os
from        common         import  date, time, UserTable, ADMIN_KEY, BOT, Back_Button
#Connect to sql databases
name_user = None

#Users
translete = str.maketrans("","",")(,][")
translete_l = str.maketrans("","",")'(][")
try:
    SQL = sqlite.connect("./DATA.DB")
    CURSOR = SQL.cursor()
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER UNIQUE NOT NULL ,
            name     VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL,
            salt     TEXT,
            lastseen DATE,
            status   VARCHAR(20) DEFAULT "Пользователь",
            balance  INTEGER    DEFAULT  5000)''')
    SQL.commit()
    CURSOR.execute("SELECT COUNT(*) FROM users")
    column_info_users = str(CURSOR.fetchall()).translate(translete)
    column_count_users = int(column_info_users)
    print(f"Количество пользователей: {column_count_users}")
    SQL.commit()
    CURSOR.execute("SELECT id FROM users")
    SQL.commit()
except Exception as e:
    print(f"Ошибка при подключении к базе данных: {e}")
finally:
    CURSOR.close()
    SQL.close()

###ADMIN SQL
try:
    SQL_ADMIN = sqlite.connect("./DATA_ADMIN.DB")
    CURSOR_ADMIN = SQL_ADMIN.cursor()
    CURSOR_ADMIN.execute('''
        CREATE TABLE IF NOT EXISTS admins (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          chat_id INTEGER UNIQUE NOT NULL
        )''')
    SQL_ADMIN.commit()
    CURSOR_ADMIN.execute("SELECT COUNT(*) FROM admins")
    column_info_admins = str(CURSOR_ADMIN.fetchall()).translate(translete)
    column_count_admins = int(column_info_admins)
    SQL_ADMIN.commit()
    CURSOR_ADMIN.execute("SELECT chat_id FROM admins")
    SQL_ADMIN.commit()
    info_admins_id = CURSOR_ADMIN.fetchall()
except Exception as e:
    print(e)
finally:
    print(f"Количество админов:{column_info_admins} ")
    CURSOR_ADMIN.close()
    SQL_ADMIN.close()



#SET from DATABASEE
def Set_user_name(name):
    global name_user
    name_user = name

def save_info_user(message, additional_arg: int):
    global column_count_users, column_count_admins, name_user
    password_user = message.text.strip()
    if len(password_user) >= 30:
         BOT.send_message(message.chat.id, "Пароль слишком длинный, повторите попытку")
    # ADMIN?
    if name_user == "ADMIN" and password_user == ADMIN_KEY:
        BOT.send_message(message.chat.id, "Вы вошли как админ")
        SQL_ADMIN = sqlite.connect("./DATA_ADMIN.DB")
        CURSOR_ADMIN = SQL_ADMIN.cursor()
        try:
            CURSOR_ADMIN.execute("INSERT INTO admins (chat_id) VALUES (?)", (message.chat.id,))
            SQL_ADMIN.commit()
            column_count_admins += 1
            session_id_admins.append(message.chat.id)
            print(f"Кто-то вошел как админ, сейчас их {column_count_admins}")
        except sqlite.Error as e:
            print(f"Ошибка при добавлении админа в базу данных: {e}")
        finally:
            CURSOR_ADMIN.close()
            SQL_ADMIN.close()
            BOT.send_message(message.chat.id, "Регистрация админа окончена")
            Back_Button(message)
            return 0
        
    SQL = sqlite.connect("./DATA.DB")
    CURSOR = SQL.cursor()
    # Generation salt
    salt = os.urandom(16).hex()
    hashed_password = hash.sha256((salt + password_user).encode()).hexdigest()
    # USER
    try:
        CURSOR.execute(f"""INSERT INTO users (id, name, password, salt, lastseen) 
VALUES (?, ?, ?, ?, ?)""", (additional_arg, name_user, hashed_password, salt, date.today(),))
        SQL.commit()
        column_count_users += 1
        BOT.send_message(message.chat.id, "Регистрация окончена")
        print(f"Новый пользователь зарегистрировался! Всего зарегистрированнно: {column_count_users}")
    except sqlite.IntegrityError:
        BOT.send_message(message.chat.id, "Имя занято или аккаунт уже создан.")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя в базу данных: {e}")
    finally:
        CURSOR.close()
        SQL.close()
        Back_Button(message)

def delete_account(message, additional_arg):
    if message.text == "ДА":
        try:
            SQL = sqlite.connect("./DATA.DB")
            CURSOR = SQL.cursor()
            CURSOR.execute("DELETE FROM users WHERE id = ?", (additional_arg,))
            SQL.commit()
            BOT.send_message(message.chat.id, "Аккаунт удален!")
            print("Удаление завершено!")
        except Exception as e:
            print(e)
        finally:
            CURSOR.close()
            SQL.close()
    else:
        BOT.send_message(message.chat.id, "Отмена операции.")

def set_skm_user(message, amount, user_id):
    try:
        with sqlite.connect("./DATA.DB") as SQL:
            CURSOR = SQL.cursor()
            CURSOR.execute('''
                UPDATE users
                SET balance = balance + ?
                WHERE id = ?''', (amount, user_id,))
            CURSOR.execute('''
                SELECT * FROM users
                WHERE id = ?''', (user_id,))
            data = CURSOR.fetchone()
            if data is None:
                return BOT.send_message(message.chat.id, "Для пополнения баланса нужно зарегистрироваться в этом боте!")
            return BOT.send_message(message.chat.id, "Успешно!")
    except Exception as e:
        print(e)
#GET all from DATABASE

def List_users():
    global CURSOR, SQL
    SQL = sqlite.connect("./DATA.DB")
    CURSOR = SQL.cursor()
    CURSOR.execute('''
    SELECT * FROM users
''')
    SQL.commit()
    users = CURSOR.fetchall()
    CURSOR.close()
    SQL.close()
    try:
        info = ""
        for el in users:
            info += f"""id: {el[0]}\n Имя: {el[1]}\n Пароль: {el[2]}
\n Соль: {el[3]}\n \n Дата последнего визита: {el[4]} \n Статус: {el[5]} \n Баланс: {el[6]}\n"""
        return info or "База пуста"
    except Exception as e:
        print(e)
        return "База пуста"
        
def List_admins():
    global CURSOR_ADMIN, SQL_ADMIN
    SQL_ADMIN = sqlite.connect("./DATA_ADMIN.DB")
    CURSOR_ADMIN = SQL_ADMIN.cursor()
    CURSOR_ADMIN.execute('''
    SELECT * FROM admins
''')
    SQL_ADMIN.commit()
    admins = CURSOR_ADMIN.fetchall()
    CURSOR_ADMIN.close()
    SQL_ADMIN.close()
    info = ""
    for el in admins:
        info += f"ID:{el[0]}\n Key:{el[1]}\n \n"
    return info

def Enter_user(message, additional_arg):
    try:
        info_list = message.text.split()
        
        if len(info_list) < 2:
            BOT.send_message(message.chat.id, "Пожалуйста, введите имя и пароль через пробел.")
            return

        username, password = info_list[0], info_list[1]
    except Exception:
        BOT.send_message(message.chat.id, "Ошибка при обработке ввода.")
        return

    SQL = sqlite.connect('DATA.DB')
    CURSOR = SQL.cursor()

    # Получение данных из базы
    CURSOR.execute("SELECT password, salt FROM users WHERE name = ?", (username,))
    result = CURSOR.fetchone()

    if result:
        password_real, salt = result[0], result[1]
        
        # Захеширование пароля с солью
        hash_password_check = hash.sha256((salt + password).encode()).hexdigest()

        # Сравнение захешированных паролей
        if password_real == hash_password_check:
            BOT.send_message(message.chat.id, "Вход выполнен!")
            print("Аутентификация прошла успешно!")

            CURSOR.execute('''
                UPDATE users
                SET lastseen = ?
                WHERE id = ?''', (date.today(), additional_arg))  

            CURSOR.execute('''
                UPDATE users
                SET id = ?
                WHERE name = ?''', (additional_arg, username))

            SQL.commit()
            CURSOR.close()
            SQL.close()
            BOT.send_message(message.chat.id, create_table(message, additional_arg), parse_mode="html")
        else:
            BOT.send_message(message.chat.id, "Неправильный пароль или имя")
            print("Неверный пароль.")
            CURSOR.close()
            SQL.close()
    else:
        BOT.send_message(message.chat.id, "Повторите попытку еще раз...")
        print("Пользователь не найден.")
        CURSOR.close()
        SQL.close()

def Reg_user_first_check(message) -> bool:
    try:
        SQL = sqlite.connect('DATA.DB')
        CURSOR = SQL.cursor()
        CURSOR.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
        user = CURSOR.fetchone()
        return user is not None
    except sqlite.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return False  
    finally:
        CURSOR.close()
        SQL.close()

def create_table(message, id):
    info_user = "None ;("
    try:
        # Используем контекстные менеджеры для работы с БД
        with sqlite.connect("./DATA.DB") as SQL:
            CURSOR = SQL.cursor()
            CURSOR.execute("SELECT name, status, balance FROM users WHERE id = ?", (id,))
            data_table = CURSOR.fetchone()
            if data_table is None:
                return "Зарегистрируйтесь в аккаунт на этом (новом) устройстве!\n\n*Одновременный вход с нескольких аккаунтов Telegram невозможен!"
            info_user = UserTable.create_table(data_table[0], data_table[1], data_table[2])
    
    except Exception as e:
        print(e)
        return "Произошла ошибка при получении данных."

    finally:
        Back_Button(message)

    return info_user
        
#ADMIN SQLS FUNC

def Add_admins()-> list[int]:
    session_id_admins = []
    for numbers in info_admins_id:
        for number in numbers:
            session_id_admins.append(int(number))
    return session_id_admins

session_id_admins = Add_admins()