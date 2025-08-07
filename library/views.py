import logging
from flask import Blueprint, jsonify

from models.book import Book
from models.borrowrecord import BorrowRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

views_bp = Blueprint('views', __name__)


###############################################################

@views_bp.route('/books/available/', methods=['GET'])
def available_books():
    books = Book.query.filter(Book.available_copies > 0).all()
    results = []
    for book in books:
        results.append({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies,
            "created_at": book.created_at,
            "updated_at": book.updated_at,
            "delete_at": book.delete_at
        })
    return jsonify(results)


#############################################################

@views_bp.route('/members/<int:member_id>/borrowed', methods=['GET'])
def borrowed_books(member_id):
    try:
        borrow_records = BorrowRecord.query.filter_by(member_id=member_id, returned_at=None).all()
        if not borrow_records:
            logger.error("У пользователя нету избранных книг")
            return jsonify({"warring": "У пользователя нету избранных книг"})

        books = []
        for record in borrow_records:
            book = Book.query.get(record.book_id)
            if book:
                books.append(book)

        if not books:
            logger.warning("Книги не найдены")
            return jsonify({"warning": "Книги не найдены"})

        results = []
        for idx, record in enumerate(borrow_records, start=1):
            book = Book.query.get(record.book_id)
            if book:
                results.append({
                    "id": idx,
                    "book_id": book.book_id,
                    "title": book.title,
                    "author": book.author,
                    "isbn": book.isbn,
                    "total_copies": book.total_copies,
                    "available_copies": book.available_copies,
                    "created_at": book.created_at,
                    "updated_at": book.updated_at,
                    "delete_at": book.delete_at,
                    "borrowed_at": record.borrowed_at,
                })

        return jsonify(results)
    except Exception as e:
        logger.error(F"Ошибка при получении взятых книг: {e}")
        return jsonify({"error": "Произошла ошибка при получении данных"})
