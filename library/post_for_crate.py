import logging
from datetime import datetime
from flask import Blueprint, request, jsonify

from db_connect import db

from models.book import Book
from models.member import Member

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

post_bp = Blueprint('post_for_create', __name__)


@post_bp.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.json

        if not isinstance(data['title'], str):
            logger.error("Ошибка при проверки назначения названия")
            raise ValueError("Ошибка при проверки назначения названия")
        title = data['title'].strip()


        if not isinstance(data['firstname'], str) or not data['firstname'].isalpha():
            logger.error("Имя должно содержать только буквы")
            raise ValueError("Имя должно содержать только буквы")
        firstname = data['firstname'].strip()

        if not isinstance(data['surname'], str) or not data['surname'].isalpha():
            logger.error("Фамилия должна содержать только буквы")
            raise ValueError("Фамилия должна содержать только буквы")
        surname = data['surname'].strip()

        author = str(firstname + " " + surname)


        if not isinstance((data['isbn']), int):
            logger.error("ISBN должен быть целым числом")
            raise ValueError("ISBN должен быть целым числом")
        isbn = (data['isbn'])

        if not isinstance(data['total_copies'], int):
            logger.error("Total copies должен быть целым числом")
            raise ValueError("Total copies должен быть целым числом")
        total_copies = (data['total_copies'])

        if not isinstance(data['available_copies'], int):
            logger.error("Available copies должен быть целым числом")
            raise ValueError("Available copies должен быть целым числом")
        available_copies = (data['available_copies'])

        created_at = datetime.now()

        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            total_copies=total_copies,
            available_copies=available_copies,
            created_at=created_at
        )

        db.session.add(book)
        db.session.commit()

        logger.info("Книга успешно создана")
        return jsonify({
            "message": "Книга успешно создана",
            "book_id": book.book_id
        })

    except BaseException as e:
        db.session.rollback()
        logger.error(f"Произошла ошибка при создании книги: {e}")
        return jsonify({"error": e})


@post_bp.route('/members', methods=['POST'])
def create_member():
    try:
        data = request.json

        if not isinstance(data['firstname'], str) or not data['firstname'].isalpha():
            logger.error("Имя должно содержать только буквы")
            raise ValueError("Имя должно содержать только буквы")
        firstname = data['firstname'].strip()

        if not isinstance(data['surname'], str) or not data['surname'].isalpha():
            logger.error("Фамилия должна содержать только буквы")
            raise ValueError("Фамилия должна содержать только буквы")
        surname = data['surname'].strip()

        name = firstname + ' ' + surname


        email = data['email'].strip()

        joined_at = datetime.now()

        member = Member(
            name=name,
            email=email,
            joined_at=joined_at
        )

        db.session.add(member)
        db.session.commit()

        logger.info("Пользователь успешно создан")
        return jsonify({
            "message": "Пользователь успешно создан",
            "member_id": member.member_id
        })

    except BaseException as e:
        db.session.rollback()
        logger.error(f"Произошла ошибка при создании пользователя: {e}")
        return jsonify({"error": e})
