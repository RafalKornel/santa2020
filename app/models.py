from . import db
from random import randint
from hashlib import md5
from flask import current_app

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    pin = db.Column(db.String(4))
    drafted_person_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @staticmethod
    def generate_pin():
        result = ""
        for _ in range(4):
            result += str(randint(0, 9))
        return result

    def __repr__(self):
        return f"<User: {self.name}>"

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.pin = User.generate_pin()


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    name_hash = db.Column(db.String(200))
    secure = db.Column(db.Boolean, default=False)
    users = db.relationship("User", backref="group")

    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

        if self.secure:
            self.name_hash = md5( (current_app.config["SECRET_KEY"] + self.name).encode("utf-8")).hexdigest()