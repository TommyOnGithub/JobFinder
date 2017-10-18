from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
import re


db = SQLAlchemy(app)

# To update/sync database to the following:
# 1. Enter python in directory containing db_model.py
# 2. Type "from db_model import db"
# 3. Type "db.create_all()"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    pwhash = db.Column(db.String())
    email = db.Column(db.String(120), nullable=True)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())
    current_session = db.Column(db.String())
    isAdmin = db.Column(db.Boolean, default=False)
    isFaculty = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def check_password(self, pw):
        return check_password_hash(self.pwhash, pw)

    def set_password(self, pw):
        self.pwhash = generate_password_hash(pw, method="pbkdf2:sha256", salt_length=8)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_strong_pass(self, pw):
        length_error = len(pw) < 8
        digit_error = re.search(r"\d", pw) is None
        uppercase_error = re.search(r"[A-Z]", pw) is None
        lowercase_error = re.search(r"[a-z]", pw) is None
        symbol_error = re.search(r"\W", pw) is None
        password_ok = not(length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
        return {
            'password_ok' : password_ok,
            'Length at least 8' : length_error,
            'At least one digit' : digit_error,
            'At least one uppercase' : uppercase_error,
            'At least one lowercase' : lowercase_error,
            'At least one symbol' : symbol_error,
        }

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill1 = db.Column(db.Integer)
    skill2 = db.Column(db.Integer)
    skill3 = db.Column(db.Integer)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

class Degree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
