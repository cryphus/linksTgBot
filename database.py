import sqlite3

def create_new_table():
    db = sqlite3.connect('users.db')
    try:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS login_id (
                id INTEGER PRIMARY KEY,
                name TEXT
            )""")
        db.commit()
    finally:
        db.close()

def show_all_link():
    db = sqlite3.connect('links.db')
    try:
        cursor = db.cursor()
        cursor.execute("SELECT name, link FROM links")
        content = cursor.fetchall()
        db.close()
        return content
    except Exception as e:
        print(f'Ошибка show_all_link. Код ошибка: {e}')

def check_on_availability(user_id, user_first_name):
    db = sqlite3.connect('users.db')
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id FROM login_id WHERE id = ?", (user_id,))
        data = cursor.fetchone()
        if data is None and user_id > 0:
            user_data = [user_id, user_first_name]
            cursor.execute("INSERT INTO login_id VALUES(?,?);", user_data)
            db.commit()
    finally:
        db.close()

def add_link(name, link):
    db = sqlite3.connect('links.db')
    try:
        cursor = db.cursor()
        # Вставляем значения только в столбцы name и link, id будет сгенерирован автоматически
        cursor.execute("INSERT INTO links (name, link) VALUES (?, ?);", (name, link))
        db.commit()
    finally:
        db.close()


def get_all_user_ids():
    conn = sqlite3.connect('users.db')  # Подключаемся к базе данных
    cursor = conn.cursor()

    # Выполняем запрос для получения всех user_id
    cursor.execute("SELECT id FROM login_id")
    user_ids = cursor.fetchall()  # Получаем все user_id

    conn.close()  # Закрываем соединение с базой данных
    return [user_id[0] for user_id in user_ids]  # Возвращаем список user_id


def delete_row_by_id(row_id):
    try:
        # Убедитесь, что row_id является целым числом
        row_id = int(row_id)

        # Подключаемся к базе данных
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()

        # SQL-запрос для удаления строки по id
        cursor.execute("DELETE FROM links WHERE id = ?", (row_id,))

        # Сохраняем изменения
        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()

    except ValueError:
        raise ValueError("Некорректный формат номера. Убедитесь, что вы вводите целое число.")


def show_all_link_for_admin():
    db = sqlite3.connect('links.db')
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, link FROM links")
        content = cursor.fetchall()
        db.close()
        return content
    except Exception as e:
        print(f'Ошибка show_all_link. Код ошибка: {e}')