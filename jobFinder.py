from flask import render_template, session, url_for, redirect, flash, request
from flask_login import LoginManager, current_user, login_user
from app import app
from db_model import db, User, Degree, Job, Skill, SkillNames
import xml.etree.ElementTree

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
        getXML()
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
    skills = getSkillData(current_user.id)
    return render_template('profile.html', user=current_user, userProfile=thisProfile)

@app.route('/updateProf', methods=['GET', 'POST'])
def updateProf():
    user_instance = db.session.query(User).filter_by(username=current_user.username).first()
    email = request.form.get('email', type=str)
    password = request.form.get('pass', type=str)
    if password != '0':
        strength = current_user.is_strong_pass(password)
        if strength['password_ok']:
            user_instance.set_password(password)
    if email != '0':
        user_instance.email = email
    db.session.commit()
    return 'Updated'

@app.route('/main', methods=['GET', 'POST'])
def main():
    majors = db.session.query(Degree.name).all()
    jobs = db.session.query(Job.name).all()
    try:
        current_user.username
    except AttributeError:
        return render_template('main.html', user=None, majors=majors, jobs=jobs)
    return render_template('main.html', user=current_user, majors=majors, jobs=jobs)


def getXML():
    jobXml = xml.etree.ElementTree.parse('jobs_data.xml').getroot()
    for jTitle in jobXml.iter('title'):
        checkExist = db.session.query(Job).filter_by(name=jTitle.text).first()
        if checkExist is None:
            job = Job()
            job.name = jTitle.text
            db.session.add(job)
            db.session.commit()

    majorXml = xml.etree.ElementTree.parse('majors_data.xml').getroot()
    for mTitle in majorXml.iter('title'):
        checkExist = db.session.query(Degree).filter_by(name=mTitle.text).first()
        if checkExist is None:
            degree = Degree()
            degree.name = mTitle.text
            db.session.add(degree)
            db.session.commit()

    skillXml1 = xml.etree.ElementTree.parse('jobs_data.xml').getroot()
    for skill in skillXml1.iter('skill'):
        checkExist = db.session.query(SkillNames).filter_by(name=skill.text.split(',')[0]).first()
        if checkExist is None:
            skillName = SkillNames()
            skillName.name = skill.text.split(',')[0]
            db.session.add(skillName)
            db.session.commit()

    skillXml2 = xml.etree.ElementTree.parse('majors_data.xml').getroot()
    for skill in skillXml2.iter('skill'):
        checkExist = db.session.query(SkillNames).filter_by(name=skill.text.split(',')[0]).first()
        if checkExist is None:
            skillName = SkillNames()
            skillName.name = skill.text.split(',')[0]
            db.session.add(skillName)
            db.session.commit()
    return


def getSkillData(id):
    resultDict = {}
    skillNames = db.session.query(SkillNames).all()
    skill = db.session.query(Skill).filter_by(id=id).first()
    for skillName in skillNames:
        holder = str(skillName)
        resultDict[skillName] = skill
    return resultDict

def search_by_degree(user, degree):
    user_skills = get_skills(user.get_skill_id())
    degree_skills = get_skills(degree.get_id())
    combined_skills = {}
    for k in user_skills.iterkeys():
        combined_skills[k] = user_skills[k] + degree_skills[k]
        if combined_skills[k] > 5:
            combined_skills[k] = 5
    jobs = get_jobs()
    #TODO

def search_by_job(user, job):
    user_skills = get_skills(user.get_skill_id())
    job_skills = get_skills(job.get_id())
    missing_skills = {}
    for k in user_skills.iterkeys():
        missing_skills[k] = job_skills[k] - user_skills[k]
        if missing_skills[k] < 0:
            missing_skills[k] = 0
    degrees = get_degrees()
    #TODO


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

