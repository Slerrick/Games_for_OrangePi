import sqlite3 as sqlite
from common import td, date

def delete_inactive_accounts():
    try:
        SQL = sqlite.connect('DATA.DB')
        CURSOR = SQL.cursor()

        current_date = date.today()

        date_threshold = current_date - td(days=190)
        
        CURSOR.execute("DELETE FROM users WHERE lastseen <= ?", (date_threshold,))
        

        deleted_count = CURSOR.rowcount
        SQL.commit()
        
        print(f"Удалено пользователей: {deleted_count}")
    except sqlite.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        CURSOR.close()
        SQL.close()

def clear_admins():
    try:
        SQL_ADMIN = sqlite.connect("./DATA_ADMIN.DB")
        CURSOR_ADMIN = SQL_ADMIN.cursor()
        CURSOR_ADMIN.execute("DELETE  FROM admins")
        SQL_ADMIN.commit()
    except Exception as e:
        print(f"Ошибка при очистке таблицы admins: {e}")
    finally:
        CURSOR_ADMIN.close()
        SQL_ADMIN.close()
        return print("Список админов удален!")
