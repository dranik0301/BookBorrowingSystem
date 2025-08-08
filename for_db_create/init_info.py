import sqlite3
import os
from dotenv import load_dotenv
from faker import Faker
import random
from datetime import datetime, timedelta


# Загружаем переменной из .env
load_dotenv()

# Получаем имя базы из .env
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Определяем путь к проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Путь до for_db_create
PROJECT_DIR = os.path.dirname(BASE_DIR) # Путь до всего проекта
DATABASE_PATH = os.path.join(PROJECT_DIR, DATABASE_NAME)

if not os.path.exists(DATABASE_NAME):
    print(f"Файл базы данных {DATABASE_NAME} не найден")
else:
    print("Файл с базой существует")

fake = Faker('ru_RU')  # Используем русскую язык для Faker


def generate_random_datetime(start_year=2024):
    """Генерирует случайную дату и время"""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime.now()
    time_between_dates = end_date - start_date
    random_number_of_days = random.randint(0, time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )


def populate_book(num_book):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    for _ in range(num_book):
        title = fake.unique.word().capitalize()
        author = f'{fake.first_name()} {fake.last_name()}'
        isbn = random.randint(1000, 9999)
        total_copies = random.randint(0, 100)
        available_copies = random.randint(0, total_copies)

        created_at = generate_random_datetime().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO book (title, author, isbn, total_copies, available_copies, created_at, updated_at, delete_at)
            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)
        """, (title, author, isbn, total_copies, available_copies, created_at))
    conn.commit()
    conn.close()
    print(f"Таблица 'book' заполнена на {num_book}")


def populate_member(num_member):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    for _ in range(num_member):
        name = f'{fake.first_name()} {fake.last_name()}'
        email = fake.unique.email()

        joined_at = generate_random_datetime().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO member (name, email, joined_at, updated_at, delete_at)
            VALUES (?, ?, ?, NULL, NULL)
        """, (name, email, joined_at))
    conn.commit()
    conn.close()
    print(f"Таблица 'member' заполнена на {num_member}")


def populate_borrowrecord(num_borrowrecord):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT book_id FROM book")
    book_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT member_id FROM member")
    member_ids = [row[0] for row in cursor.fetchall()]

    if not member_ids:
        print("В таблице 'member' нет записей")
        conn.close()
        return

    if not book_ids:
        print("В таблице 'book' нет записей")
        conn.close()
        return

    for _ in range(num_borrowrecord):
        member_id = random.choice(member_ids)
        book_id = random.choice(book_ids)

        borrowed_at = generate_random_datetime().strftime('%Y-%m-%d %H:%M:%S')

        if random.choice([True, False]):
            returned_at = generate_random_datetime().strftime('%Y-%m-%d %H:%M:%S')
        else:
            returned_at = None

        # returned_at = generate_random_datetime().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO borrowrecord (member_id, book_id, borrowed_at, returned_at)
            VALUES (?, ?, ?, ?)
        """, (member_id, book_id, borrowed_at, returned_at))

    conn.commit()
    conn.close()
    print(f"Таблица 'borrowrecord' заполнена на {num_borrowrecord}")


if __name__ == "__main__":
    # Заполняем таблицы в логическом порядке
    # populate_book(5)
    # populate_member(5)
    # populate_borrowrecord(5)
    pass
