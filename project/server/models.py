from project.server.log import INFO

import datetime

from project.server import db

from sqlalchemy.schema import UniqueConstraint


# TODO remove..
class Example(db.Model):
    __tablename__ = "example"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, field):
        self.field = field


class Picture(db.Model):
    __tablename__ = "picture_meatadata"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    # represents a user name in auth db
    creator = db.Column(db.String(255), nullable=False)
    __table_args__ = (UniqueConstraint('title', 'creator', name='_title_creator_uc'),)

    def __init__(self, title, creator):
        self.title = title
        self.creator = creator
