# Library API

Это простой API для библиотеки, работающий локально по адресу:  
http://127.0.0.1:5000

---

## POST /books — Добавить новую книгу  
**URL:** http://127.0.0.1:5000/books  
**Пример запроса:**
```bash
curl -X POST http://127.0.0.1:5000/books -H "Content-Type: application/json" -d '{
  "title": "1984",
  "firstname": "George",
  "surname": "Orwell",
  "isbn": 123456789,
  "total_copies": 5,
  "available_copies": 5
}'
```

---

## POST /members — Зарегистрировать нового пользователя  
**URL:** http://127.0.0.1:5000/members  
**Пример запроса:**
```bash
curl -X POST http://127.0.0.1:5000/members -H "Content-Type: application/json" -d '{
  "firstname": "Alice",
  "surname": "Smith",
  "email": "alice@example.com"
}'
```

---

## POST /borrow — Взять книгу  
**URL:** http://127.0.0.1:5000/borrow  
**Пример запроса:**
```bash
curl -X POST http://127.0.0.1:5000/borrow -H "Content-Type: application/json" -d '{
  "member_id": 1,
  "book_id": 1
}'
```

---

## POST /return — Вернуть книгу  
**URL:** http://127.0.0.1:5000/return  
**Пример запроса:**
```bash
curl -X POST http://127.0.0.1:5000/return -H "Content-Type: application/json" -d '{
  "order_id": 1
}'
```

---

## GET /books/available — Посмотреть все доступные книги  
**URL:** http://127.0.0.1:5000/books/available  
**Пример запроса:**
```bash
curl http://127.0.0.1:5000/books/available
```

---

## GET /members/<id>/borrowed — Посмотреть книги, которые взял пользователь  
**URL:** http://127.0.0.1:5000/members/<id>/borrowed  
Пример для пользователя с ID 1:
```bash
curl http://127.0.0.1:5000/members/1/borrowed
```

---

## Запуск проекта

1. Убедитесь, что у вас установлен Flask и база данных настроена.
2. Запустите сервер командой:
```bash
flask run
```
или
```bash
python app.py
```
3. После этого можно использовать запросы выше для работы с API.
