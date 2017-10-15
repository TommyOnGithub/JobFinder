from flask import render_template, session, url_for, redirect, flash, request
from flask_login import LoginManager, current_user, login_user
from app import app
from db_model import db, User

login_manager = LoginManager()
login_manager.init_app(app)

# Sometimes socket will not close properly if you are turning off/on rapidly/while editing
# Type "fuser -k 5000/tcp" into terminal to fix

# To update/sync database to the following:
# 1. Enter python in directory containing db_model.py
# 2. Type "from db_model import db"
# 3. Type "db.create_all()"

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def toLogin():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import register_form
    form = register_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        strength = user.is_strong_pass(form.password.data)
        if strength['password_ok']:
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            for key, value in strength.iteritems():
                if value:
                    flash(key)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import login_form
    form = login_form(request.form)
    if request.method == 'POST' and form.validate():
        user = form.get_user()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('login.html', form=form, session=session)


@app.route('/logout')
def logout():
    '''Logs out a user by clearing session information'''
    session.clear()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    thisProfile = []
    thisProfile.insert(0, {'username': current_user.username, 'email': current_user.email,
                           'firstName': current_user.firstName, 'lastName': current_user.lastName})
    return render_template('profile.html', user=current_user, userProfile=thisProfile)

@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html', user=current_user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

