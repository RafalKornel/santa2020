from . import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    def __repr__(self):
        return f"<User: {self.name}>"

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    key = db.Column(db.String(32), unique=True)
    users = db.relationship("User", backref="group")