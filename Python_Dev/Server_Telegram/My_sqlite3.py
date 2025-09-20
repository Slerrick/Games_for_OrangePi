import sqlite3
import hashlib
import os
from common import date, UserTable, ADMIN_KEY, BOT, back_button
from typing import Optional, List, Tuple

# Глобальные переменные
name_user: Optional[str] = None
column_count_users: int = 0
column_count_admins: int = 0
info_admins_id: List[Tuple[int]] = []
session_id_admins: List[int] = []

class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()

def initialize_databases():
    """Инициализация баз данных"""
    global column_count_users, column_count_admins, info_admins_id
    
    # База пользователей
    try:
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER UNIQUE NOT NULL,
                    name VARCHAR(20) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    salt TEXT,
                    lastseen DATE,
                    status VARCHAR(20) DEFAULT "Пользователь",
                    balance INTEGER DEFAULT 5000
                )''')
            
            cursor.execute("SELECT COUNT(*) FROM users")
            column_count_users = cursor.fetchone()[0]
            print(f"Количество пользователей: {column_count_users}")
            
    except Exception as e:
        print(f"Ошибка при инициализации базы пользователей: {e}")
    
    # База администраторов
    try:
        with DatabaseManager("./DATA_ADMIN.DB") as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER UNIQUE NOT NULL
                )''')
            
            cursor.execute("SELECT COUNT(*) FROM admins")
            column_count_admins = cursor.fetchone()[0]
            
            cursor.execute("SELECT chat_id FROM admins")
            info_admins_id = cursor.fetchall()
            
    except Exception as e:
        print(f"Ошибка при инициализации базы администраторов: {e}")
    
    print(f"Количество админов: {column_count_admins}")

def set_user_name(name: str):
    """Установка имени пользователя"""
    global name_user
    name_user = name

def save_info_user(message, additional_arg: int):
    """Сохранение информации о пользователе"""
    global column_count_users, column_count_admins, name_user
    
    password_user = message.text.strip()
    
    if len(password_user) >= 30:
        BOT.send_message(message.chat.id, "Пароль слишком длинный, повторите попытку")
        return
    
    # Проверка на администратора
    if name_user == "ADMIN" and password_user == ADMIN_KEY:
        try:
            with DatabaseManager("./DATA_ADMIN.DB") as cursor:
                cursor.execute("INSERT INTO admins (chat_id) VALUES (?)", (message.chat.id,))
                column_count_admins += 1
                session_id_admins.append(message.chat.id)
                print(f"Кто-то вошел как админ, сейчас их {column_count_admins}")
                
            BOT.send_message(message.chat.id, "Вы вошли как админ")
            BOT.send_message(message.chat.id, "Регистрация админа окончена")
            
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении админа: {e}")
            BOT.send_message(message.chat.id, "Ошибка при регистрации админа")
        
        finally:
            back_button(message)
        return
    
    # Регистрация обычного пользователя
    salt = os.urandom(16).hex()
    hashed_password = hashlib.sha256((salt + password_user).encode()).hexdigest()
    
    try:
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute(
                "INSERT INTO users (id, name, password, salt, lastseen) VALUES (?, ?, ?, ?, ?)",
                (additional_arg, name_user, hashed_password, salt, date.today())
            )
            column_count_users += 1
            BOT.send_message(message.chat.id, "Регистрация окончена")
            print(f"Новый пользователь зарегистрировался! Всего: {column_count_users}")
            
    except sqlite3.IntegrityError:
        BOT.send_message(message.chat.id, "Имя занято или аккаунт уже создан.")
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        BOT.send_message(message.chat.id, "Ошибка при регистрации")
    
    finally:
        back_button(message)

def delete_account(message, additional_arg: int):
    """Удаление аккаунта"""
    if message.text.upper() == "ДА":
        try:
            with DatabaseManager("./DATA.DB") as cursor:
                cursor.execute("DELETE FROM users WHERE id = ?", (additional_arg,))
                BOT.send_message(message.chat.id, "Аккаунт удален!")
                print("Удаление завершено!")
                
        except Exception as e:
            print(f"Ошибка при удалении аккаунта: {e}")
            BOT.send_message(message.chat.id, "Ошибка при удалении аккаунта")
    else:
        BOT.send_message(message.chat.id, "Отмена операции.")

def set_skm_user(message, amount: int, user_id: int):
    """Пополнение баланса пользователя"""
    try:
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE id = ?",
                (amount, user_id)
            )
            
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            data = cursor.fetchone()
            
            if data is None:
                return BOT.send_message(message.chat.id, "Для пополнения баланса нужно зарегистрироваться!")
            
            return BOT.send_message(message.chat.id, "Успешно!")
            
    except Exception as e:
        print(f"Ошибка при пополнении баланса: {e}")
        BOT.send_message(message.chat.id, "Ошибка при пополнении баланса")

def list_users() -> str:
    """Получение списка всех пользователей"""
    try:
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            
            if not users:
                return "База пуста"
                
            info_lines = []
            for user in users:
                info_lines.append(
                    f"id: {user[0]}\nИмя: {user[1]}\nПароль: {user[2]}\n"
                    f"Соль: {user[3]}\nДата последнего визита: {user[4]}\n"
                    f"Статус: {user[5]}\nБаланс: {user[6]}\n"
                )
            
            return "\n".join(info_lines)
            
    except Exception as e:
        print(f"Ошибка при получении списка пользователей: {e}")
        return "Ошибка при получении данных"

def list_admins() -> str:
    """Получение списка администраторов"""
    try:
        with DatabaseManager("./DATA_ADMIN.DB") as cursor:
            cursor.execute("SELECT * FROM admins")
            admins = cursor.fetchall()
            
            if not admins:
                return "Администраторы не найдены"
                
            info_lines = []
            for admin in admins:
                info_lines.append(f"ID:{admin[0]}\nKey:{admin[1]}\n")
            
            return "\n".join(info_lines)
            
    except Exception as e:
        print(f"Ошибка при получении списка администраторов: {e}")
        return "Ошибка при получении данных"

def enter_user(message, additional_arg: int):
    """Авторизация пользователя"""
    try:
        info_list = message.text.split()
        
        if len(info_list) < 2:
            BOT.send_message(message.chat.id, "Пожалуйста, введите имя и пароль через пробел.")
            return
        
        username, password = info_list[0], info_list[1]
        
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute("SELECT password, salt FROM users WHERE name = ?", (username,))
            result = cursor.fetchone()
            
            if not result:
                BOT.send_message(message.chat.id, "Пользователь не найден")
                return
            
            password_real, salt = result
            
            hash_password_check = hashlib.sha256((salt + password).encode()).hexdigest()
            
            if password_real == hash_password_check:
                BOT.send_message(message.chat.id, "Вход выполнен!")
                print("Аутентификация прошла успешно!")
                
                cursor.execute(
                    "UPDATE users SET lastseen = ?, id = ? WHERE name = ?",
                    (date.today(), additional_arg, username)
                )
                
                BOT.send_message(message.chat.id, create_table(message, additional_arg), parse_mode="html")
            else:
                BOT.send_message(message.chat.id, "Неправильный пароль или имя")
                print("Неверный пароль.")
                
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        BOT.send_message(message.chat.id, "Ошибка при авторизации")

def reg_user_first_check(message) -> bool:
    """Проверка существования пользователя"""
    try:
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (message.from_user.id,))
            user = cursor.fetchone()
            return user is not None
            
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False

def create_table(message, user_id: int) -> str:
    """Создание таблицы с информацией о пользователе"""
    try:
        with DatabaseManager("./DATA.DB") as cursor:
            cursor.execute(
                "SELECT name, status, balance FROM users WHERE id = ?",
                (user_id,)
            )
            data_table = cursor.fetchone()
            
            if not data_table:
                return "Зарегистрируйтесь в аккаунт на этом устройстве!\n\n*Одновременный вход с нескольких аккаунтов Telegram невозможен!"
            
            return UserTable.create_table(data_table[0], data_table[1], data_table[2])
            
    except Exception as e:
        print(f"Ошибка при создании таблицы пользователя: {e}")
        return "Произошла ошибка при получении данных."
    
    finally:
        back_button(message)

def add_admins() -> List[int]:
    """Добавление администраторов в сессию"""
    session_admins = []
    for numbers in info_admins_id:
        for number in numbers:
            session_admins.append(int(number))
    return session_admins

# Инициализация баз данных
initialize_databases()
session_id_admins = add_admins()