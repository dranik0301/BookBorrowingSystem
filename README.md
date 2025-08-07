Запуск проекта

1. Установите нужные библиотеки:

pip install -r requirements.txt

2. Запустите проект:

python app.py

---

POST /books — Добавить новую книгу

http://127.0.0.1:5000/books

Пример запроса:

{
"title": "1984",
"firstname": "George",
"surname": "Orwell",
"isbn": 123456789,
"total_copies": 5,
"available_copies": 5
}

---

POST /members — Зарегистрировать нового пользователя  

http://127.0.0.1:5000/members  

Пример запроса:

{
"firstname": "Alice",
"surname": "Smith",
"email": "alice@example.com"
}

---

POST /borrow — Взять книгу

http://127.0.0.1:5000/borrow  

Пример запроса:

{
"member_id": 1,
"book_id": 1
}

---

POST /return — Вернуть книгу

http://127.0.0.1:5000/return  

Пример запроса:

{
"order_id": 1
}'

---

GET /books/available — Посмотреть все доступные книги
Пример запроса:

http://127.0.0.1:5000/books/available

---

GET /members/<id>/borrowed — Посмотреть книги, которые взял пользователь

http://127.0.0.1:5000/members/<id>/borrowed  

Пример для пользователя с ID 1:

http://127.0.0.1:5000/members/1/borrowed

