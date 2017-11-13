from ast import literal_eval
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
import re


db = SQLAlchemy(app)

# To update/sync database to the following:
# 1. Enter python in directory containing db_model.py
# 2. Type "from db_model import db"
# 3. Type "db.drop_all()"
# 4. Type "db.create_all()"


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
    recent_search = db.Column(db.String())
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

    def get_recent_search(self):
        resultList = []
        for i in self.recent_search.split(";"):
            resultList.append(literal_eval(i))
        return resultList

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
    process_automation = db.Column(db.Integer, default=0)
    information_security = db.Column(db.Integer, default=0)
    model_view_controller = db.Column(db.Integer, default=0)
    windows_operating_system = db.Column(db.Integer, default=0)
    database_security = db.Column(db.Integer, default=0)
    networking_protocols = db.Column(db.Integer, default=0)
    troubleshooting = db.Column(db.Integer, default=0)
    unix_experience = db.Column(db.Integer, default=0)
    software_engineering_best_practices = db.Column(db.Integer, default=0)
    web_development = db.Column(db.Integer, default=0)
    software_design = db.Column(db.Integer, default=0)
    data_maintenance = db.Column(db.Integer, default=0)
    java = db.Column(db.Integer, default=0)
    software_optimization = db.Column(db.Integer, default=0)
    software_systems = db.Column(db.Integer, default=0)
    mobile_development_lifecycle = db.Column(db.Integer, default=0)
    android_sdk = db.Column(db.Integer, default=0)
    rest_api = db.Column(db.Integer, default=0)
    functional_programming_languages = db.Column(db.Integer, default=0)
    database_performance_tuning = db.Column(db.Integer, default=0)
    graphic_design = db.Column(db.Integer, default=0)
    database_management = db.Column(db.Integer, default=0)
    object_oriented_development = db.Column(db.Integer, default=0)
    compiler_design = db.Column(db.Integer, default=0)
    sql_server = db.Column(db.Integer, default=0)
    quantitative_reasoning = db.Column(db.Integer, default=0)
    electrical_engineering = db.Column(db.Integer, default=0)
    analyzing_information = db.Column(db.Integer, default=0)
    json = db.Column(db.Integer, default=0)
    software_development_fundamentals = db.Column(db.Integer, default=0)
    software_documentation = db.Column(db.Integer, default=0)
    coding_experience = db.Column(db.Integer, default=0)
    operating_system = db.Column(db.Integer, default=0)
    programming_languages = db.Column(db.Integer, default=0)
    unit_testing = db.Column(db.Integer, default=0)
    software_engineering = db.Column(db.Integer, default=0)
    technical_writing = db.Column(db.Integer, default=0)
    hardware_systems = db.Column(db.Integer, default=0)
    object_oriented_programming_languages = db.Column(db.Integer, default=0)
    uml_modeling = db.Column(db.Integer, default=0)
    declarative_programming_languages = db.Column(db.Integer, default=0)
    procedural_programming_languages = db.Column(db.Integer, default=0)
    web_frameworks = db.Column(db.Integer, default=0)
    software_development = db.Column(db.Integer, default=0)
    dot_net_programming = db.Column(db.Integer, default=0)
    written_and_verbal_communication = db.Column(db.Integer, default=0)
    operating_systems = db.Column(db.Integer, default=0)
    android_os = db.Column(db.Integer, default=0)
    software_testing = db.Column(db.Integer, default=0)
    distributed_systems = db.Column(db.Integer, default=0)
    


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

    def get_name(self):
        return self.name

class Degree(db.Model):
    __tablename__ = 'degree'
    id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    name = db.Column(db.String(), primary_key=True)
    skills = db.relationship("Skill")

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

class List(db.Model):
    __tablename__ = 'list'
    name = db.Column(db.String(), primary_key=True)


class Search(db.Model):
    __tableName__ = 'search'
    search_number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    using = db.Column(db.String())
    user = db.relationship("User")
    
