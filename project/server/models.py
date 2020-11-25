from project.server.log import INFO

import datetime

from project.server import app, db


class Example(db.Model):
    __tablename__ = "example"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, field):
        self.field = field
