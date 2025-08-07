import sqlite3
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем имя базы данных из .env
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Определяем путь к проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Путь до for_db_create
PROJECT_DIR = os.path.dirname(BASE_DIR) # Путь до всего проекта
DATABASE_PATH = os.path.join(PROJECT_DIR, DATABASE_NAME)

if not os.path.exists(DATABASE_PATH):
    print(f"Файл базы данных {DATABASE_NAME} не найден. Он будет создан автоматически.")

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()


def table_exists(table_name: str) -> bool:
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table_name,)
    )
    return cursor.fetchone() is not None


def create_tables():
    tables = ["book", "member", "borrowrecord"]

    if all(table_exists(table) for table in tables):
        print("Все таблицы уже существуют. Пропускаем создание.")
        return

    # Таблица книг
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            author TEXT,
            isbn INTEGER UNIQUE,
            total_copies INTEGER,
            available_copies INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            delete_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            delete_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Таблица заказов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowrecord (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            book_id INTEGER,
            
            borrowed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            returned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (member_id) REFERENCES member(member_id),
            FOREIGN KEY (book_id) REFERENCES book(book_id)
        )
    """)

    conn.commit()
    conn.close()
    print("Таблицы базы данных успешно созданы.")


if __name__ == "__main__":
    create_tables()
