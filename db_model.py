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
    __tablename__ =  'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    pwhash = db.Column(db.String())
    email = db.Column(db.String(120), nullable=True)
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())
    current_session = db.Column(db.String())
    isAdmin = db.Column(db.Boolean, default=False)
    isFaculty = db.Column(db.Boolean, default=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skills = db.relationship("Skill")

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

    def get_skill_id(self):
	return self.skill_id

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
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    object_oriented_development = db.Column(db.Integer)
    programming_java = db.Column(db.Integer)
    programming_cpp = db.Column(db.Integer)
    web_development = db.Column(db.Integer)
    web_frameworks = db.Column(db.Integer)
    model_view_controller_pattern = db.Column(db.Integer)
    programming_javascript = db.Column(db.Integer)
    database_management = db.Column(db.Integer)
    database_development = db.Column(db.Integer)
    networking = db.Column(db.Integer)
    distributed_systems = db.Column(db.Integer)
    android_development = db.Column(db.Integer)
    ios_development = db.Column(db.Integer)
    technical_writing = db.Column(db.Integer)
    communication = db.Column(db.Integer)
    data_analysis = db.Column(db.Integer)
    algorithm_design = db.Column(db.Integer)
    software_testing = db.Column(db.Integer)
    software_design_patterns = db.Column(db.Integer)
    software_development_fundamentals = db.Column(db.Integer)
    uml_documentation = db.Column(db.Integer)
    windows_os = db.Column(db.Integer)
    mac_os = db.Column(db.Integer)
    linux = db.Column(db.Integer)
    dot_net = db.Column(db.Integer)
    troubleshooting = db.Column(db.Integer)
    artificial_intelligence = db.Column(db.Integer)


class SkillNames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    name = db.Column(db.String(), primary_key=True)
    skills = db.relationship("Skill")

    def get_id(self):
        return self.id


class Degree(db.Model):
    __tablename__ = 'degree'
    id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    name = db.Column(db.String(), primary_key=True)
    skills = db.relationship("Skill")

    def get_id(self):
        return self.id

class List(db.Model):
    __tablename__ = 'list'
    name = db.Column(db.String(), primary_key=True)
