import logging
from datetime import datetime
from flask import Blueprint, request, jsonify

from db_connect import db

from models.book import Book
from models.borrowrecord import BorrowRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

services_bp = Blueprint('services', __name__)


######################################

def check_available_books(book_id: int) -> bool:
    try:
        book = Book.query.get(book_id)
        if book.available_copies is None:
            logger.warning(f"Книга с id={book.book_id} не найдена")
            return False

        if book.available_copies <= 0:
            logger.info("Нет книга в наличии")
            return False

        logger.info("Есть книга в наличии")
        return True

    except BaseException:
        logger.error(f"Ошибка при проверке наличия книги")
        return False


@services_bp.route('/borrow', methods=['POST'])
def borrow_book():
    """
    Проверить, есть ли доступные копии книги.
    Создать запись BorrowRecord.
    Уменьшить available_copies.
    """
    try:
        data = request.json
        member_id = data.get('member_id')
        book_id = data.get('book_id')

        if not member_id or not book_id:
            logger.error("Нету member_id или book_id")
            return jsonify({"error": "member_id и book_id обязательны"})

        book = Book.query.get(book_id)
        if not book:
            logger.error("Книга не найдена")
            return jsonify({"error": "Книга не найдена"})

        if not check_available_books(book_id):
            logger.error("Не может взять книгу, так как нет в наличии")
            return jsonify({"error": "Книга не доступна для получения"})

        logger.info("Книга доступна")
        book.available_copies -= 1

        borrow_record = BorrowRecord(
            member_id=member_id,
            book_id=book_id,
            borrowed_at=datetime.now(),
            returned_at=None
        )
        db.session.add(borrow_record)
        db.session.commit()

        logger.info("Книга успешно взята")
        return jsonify({
            "message": "Книга успешно взята",
            "order_id": borrow_record.order_id
        })
    except BaseException as e:
        db.session.rollback()
        logger.error(f"Ошибка при оформлении выдачи книги: {e}")
        return jsonify({"error": e})


######################################


@services_bp.route('/return', methods=['POST'])
def return_book():
    """
    Отметить дату возврата (returned_at).
    Увеличить available_copies.
    """
    try:
        data = request.json
        borrow_record_id = data.get("order_id")

        if borrow_record_id is None:
            logger.error("Не написали order_id")
            return jsonify({"error": "order_id обязателен"})

        record = BorrowRecord.query.get(borrow_record_id)
        if not record:
            logger.error(f"Запись с order_id {borrow_record_id} не найдена")
            return jsonify({
                "error": "Запись не найдена",
                "order_id": borrow_record_id
            })

        if record.returned_at is not None:
            logger.error(f"Книга с записью order_id {borrow_record_id} уже возвращена")
            return jsonify({
                "error": "Книга уже возвращена"
            })

        book = Book.query.get(record.book_id)
        book.available_copies += 1
        returned_at = datetime.now()

        borrow_record = BorrowRecord(
            member_id=record.member_id,
            book_id=book.book_id,
            borrowed_at=record.borrowed_at,
            returned_at=returned_at
        )

        db.session.add(borrow_record)
        db.session.commit()
        logger.info(f"Книга успешно возвращена")
        return jsonify({"message": "Книга успешно возвращена"})

    except Exception as e:
        db.session.rollback()
        logger.error(f"Ошибка при возврате книги с записью order_id: {borrow_record_id}")
        return jsonify({"error": e})

######################################
