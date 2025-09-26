import sqlite3
import os

# Абсолютный путь к файлу базы рядом с init_db.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "users.db")

print("Создаём базу данных по пути:", db_path)

# Подключение к базе (создаст файл, если его нет)
conn = sqlite3.connect(db_path)

# Создаём таблицу пользователей
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("База данных успешно создана!")
