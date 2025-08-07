from db_connect import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'book'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.Float, nullable=False, unique=True)

    total_copies = db.Column(db.Float, nullable=False)
    available_copies = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime)
