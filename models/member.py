from db_connect import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = 'member'

    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    updated_at = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime)
