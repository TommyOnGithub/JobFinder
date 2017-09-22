from wtforms import Form, validators, StringField, PasswordField
from db_model import db, User
import flask.ext.wtf.html5 as html5

class register_form(Form):
    username = StringField(label='Username', validators=[validators.InputRequired()])
    password = PasswordField(label='Password', validators=[validators.InputRequired(), validators.equal_to('confirm', message='Passwords must match')])
    confirm = PasswordField(label='Confirm Password', validators=[validators.InputRequired()])
    firstName = StringField(label='First Name', validators=[validators.InputRequired()])
    lastName = StringField(label='Last Name', validators=[validators.InputRequired()])
    email = html5.EmailField(label='Email', validators=[validators.InputRequired()])


    def validate(self):
        if not Form.validate(self):
            return False

        if db.session.query(User).filter_by(username=self.username.data).count() > 0:
            self.username.errors.append('User already exists')
            return False

        return True

class login_form(Form):
    username = StringField(label='Username', validators=[validators.InputRequired()])
    password = PasswordField(label='Password', validators=[validators.InputRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        user = self.get_user()

        if user is None:
            self.username.errors.append('Login Failed')
            #self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Login Failed')
            #self.password.errors.append('Invalid password')
            return False

        return True

    def get_user(self):
        return db.session.query(User).filter_by(username=self.username.data).first()