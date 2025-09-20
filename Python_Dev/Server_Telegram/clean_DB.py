from common import td, date, sqlite3

def delete_inactive_accounts():
    """Удаление неактивных аккаунтов"""
    try:
        with sqlite3.connect('DATA.DB') as conn:
            cursor = conn.cursor()
            
            current_date = date.today()
            date_threshold = current_date - td(days=190)
            
            cursor.execute(
                "DELETE FROM users WHERE lastseen <= ?",
                (date_threshold,)
            )
            deleted_count = cursor.rowcount
            conn.commit()
            
            print(f"Удалено пользователей: {deleted_count}")
            
    except sqlite3.Error as e:
        print(f"Ошибка при удалении неактивных аккаунтов: {e}")

def clear_admins():
    """Очистка таблицы администраторов"""
    try:
        with sqlite3.connect("./DATA_ADMIN.DB") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admins")
            conn.commit()
            print("Список админов очищен!")
            
    except Exception as e:
        print(f"Ошибка при очистке таблицы admins: {e}")