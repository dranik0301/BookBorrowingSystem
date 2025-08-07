from db_connect import db


class BorrowRecord(db.Model):
    __tablename__ = 'borrowrecord'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    member_id = db.Column(db.Integer, db.ForeignKey('users.member_id'), index=True, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), index=True, nullable=False)

    borrowed_at = db.Column(db.DateTime)
    returned_at = db.Column(db.DateTime)
