from flask import render_template, session, url_for, redirect, flash, request
from flask_login import LoginManager, current_user, login_user, login_required
from app import app
import json
from db_model import db, User, Degree, Job, Skill, SkillNames, Search
import xml.etree.ElementTree
import csv

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

def getDegree(degree_id):
    return db.session.query(Degree).get(degree_id)

def getJob(job_id):
    return db.session.query(Job).get(job_id)

@app.route('/', methods=['GET', 'POST'])
def toLogin():
    return redirect(url_for('main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import register_form
    form = register_form(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        form.populate_obj(user)
        strength = user.is_strong_pass(form.password.data)
        if strength['password_ok']:
            userSkill = Skill()
            db.session.add(userSkill)
            db.session.flush()
            user.set_password(form.password.data)
            user.skill_id = db.session.query(Skill).filter_by(id=userSkill.id).first().id
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
    if current_user.ghosting:
        current_user.ghosting = None
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        session.clear()
        return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    thisProfile = []
    studentList = db.session.query(User).filter_by(isAdmin=0).all()
    if current_user.ghosting:
        ghostID = current_user.ghosting
        try:
            ghostUser = db.session.query(User).filter_by(id=ghostID).first()
        except AttributeError:
            current_user.ghosting = None
            db.session.commit()
            thisProfile.insert(0, {'username': current_user.username, 'email': current_user.email,
                                   'firstName': current_user.firstName, 'lastName': current_user.lastName})
            skills = getSkillData(current_user.skill_id)
            return render_template('profile.html', user=current_user, userProfile=thisProfile, skills=skills,
                                   studentList=studentList, ghost=0)
        thisProfile.insert(0, {'username': ghostUser.username, 'email': ghostUser.email,
                               'firstName': ghostUser.firstName, 'lastName': ghostUser.lastName})
        skills = getSkillData(ghostUser.skill_id)
        return render_template('profile.html', user=ghostUser, userProfile=thisProfile, skills=skills,
                               studentList=studentList, ghost=1)
    else:
        thisProfile.insert(0, {'username': current_user.username, 'email': current_user.email,
                               'firstName': current_user.firstName, 'lastName': current_user.lastName})
        skills = getSkillData(current_user.skill_id)
        return render_template('profile.html', user=current_user, userProfile=thisProfile, skills=skills,
                               studentList=studentList, ghost=0)


@app.route('/loginAsUser', methods=['GET', 'POST'])
@login_required
def loginAsUser():
    if current_user.isFaculty == 0:
        return
    targetUser = request.form.get('user', type=str)
    targetUser = db.session.query(User).filter_by(username=targetUser).first()
    current_user.ghosting = targetUser.id
    db.session.commit()
    return 'User Switched'

@app.route('/statistics', methods=['GET', 'POST'])
@login_required
def statistics():
    stats = get_search_history()
    return json.dumps(stats)

@app.route('/setFaculty', methods=['GET', 'POST'])
@login_required
def setFaculty():
    targetUser = request.form.get('user', type=str)
    status = request.form.get('set', type=int)
    targetUser = db.session.query(User).filter_by(username=targetUser).first()
    if status == 1:
        targetUser.isFaculty = 1
    else:
        targetUser.isFaculty = 0
    db.session.commit()
    return 'Faculty Set'

@app.route('/updateProf', methods=['GET', 'POST'])
def updateProf():
    user_instance = db.session.query(User).filter_by(username=current_user.username).first()
    email = request.form.get('email', type=str)
    skills = request.form.get('skills', type=str)
    skills = json.loads(skills)
    '''
    if password != '0' and password is not None:
        strength = current_user.is_strong_pass(password)
        if strength['password_ok']:
            user_instance.set_password(password)
    '''
    setSkills(user_instance, skills);
    if email != '0' and email is not None:
        user_instance.email = email
    db.session.commit()
    return 'Updated'

@app.route('/deleteUser', methods=['GET', 'POST'])
@login_required
def deleteUser():
    deleteUser = current_user
    searches = db.session.query(Search).filter_by(user_id=deleteUser.id).all()
    for search in searches:
        db.session.delete(search)

    db.session.delete(deleteUser)
    skill = db.session.query(Skill).filter_by(id=deleteUser.skill_id).first()
    db.session.delete(skill)
    db.session.commit()
    return 'deleted'

@app.route('/deleteTarget', methods=['GET', 'POST'])
@login_required
def deleteTarget():
    targetUser = request.form.get('user', type=str)
    targetUser = db.session.query(User).filter_by(username=targetUser).first()
    db.session.delete(targetUser)
    db.session.commit()
    return 'Deleted'

@app.route('/main', methods=['GET', 'POST'])
def main():
    getXML()
    majors = db.session.query(Degree).all()
    jobs = db.session.query(Job).all()
    try:
        current_user.username
    except AttributeError:
        return render_template('main.html', user=None, majors=majors, jobs=jobs)
    if current_user.ghosting:
        ghostUser = db.session.query(User).filter_by(id=current_user.ghosting).first()
        return render_template('main.html', user=ghostUser, majors=majors, jobs=jobs)
    else:
        return render_template('main.html', user=current_user, majors=majors, jobs=jobs)

@app.route('/runMatch', methods=['GET', 'POST'])
@login_required
def runMatch():
    name = request.form.get('name', type=str)
    name = name.split(' - ')
    if current_user.ghosting:
        ghostUser = db.session.query(User).filter_by(id=current_user.ghosting).first()
        if name[0] == 'Degree':
            search_by_degree(ghostUser, db.session.query(Degree).filter_by(name=name[1]).first())
        elif name[0] == 'Job':
            search_by_job(ghostUser, db.session.query(Job).filter_by(name=name[1]).first())
    else:
        if name[0] == 'Degree':
            search_by_degree(current_user, db.session.query(Degree).filter_by(name=name[1]).first())
        elif name[0] == 'Job':
            search_by_job(current_user, db.session.query(Job).filter_by(name=name[1]).first())
    return 'Matched'

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    if current_user.ghosting:
        ghostUser = db.session.query(User).filter_by(id=current_user.ghosting).first()
        try:
            params = get_search_params(ghostUser.id)
            results = ghostUser.get_recent_search()
        except TypeError:
            results = ''
            params = 'No Search Found'
        return render_template('results.html', user=ghostUser, results=results, params=params)
    else:
        try:
            params = get_search_params(current_user.id)
            results = current_user.get_recent_search()
        except TypeError:
            results = ''
            params = 'No Search Found'
        return render_template('results.html', user=current_user, results=results, params=params)


def setSkills(userInst, skills):
    skillDB = db.session.query(Skill).filter_by(id=userInst.skill_id).first()
    for key, value in skills.iteritems():
        attribute = setattr(skillDB, key, int(value))
    db.session.commit()


def getXML():
    jobXml = xml.etree.ElementTree.parse('jobs_data.xml').getroot()
    for job in jobXml.findall('job'):
        checkExist = db.session.query(Job).filter_by(name=job.find('title').text).first()
        if checkExist is None:
            skillTab = Skill()
            for skill in job.find('requirements').findall('skill'):
                temp = skill.text.split(',')[0].replace(' ', '_')
                temp = temp.replace('/', '_')
                temp = temp.replace('+', 'p')
                temp = temp.lower()
                attribute = setattr(skillTab, temp, int(skill.text.split(',')[1]))
            db.session.add(skillTab)
            db.session.flush()
            jobSkills = db.session.query(Skill).filter_by(id=skillTab.id).first()
            jobTab = Job()
            jobTab.name = job.find('title').text
            jobTab.description = job.find('description').text
            jobTab.id = jobSkills.id
            db.session.add(jobTab)
            db.session.commit()

    majorXml = xml.etree.ElementTree.parse('majors_data.xml').getroot()
    for major in majorXml.findall('major'):
        checkExist = db.session.query(Degree).filter_by(name=major.find('title').text).first()
        if checkExist is None:
            skillTab = Skill()
            for skill in major.find('requirements').findall('skill'):
                temp = skill.text.replace(' ', '_')
                temp = temp.replace('/', '_')
                temp = temp.replace('+', 'p')
                temp = temp.lower()
                attribute = setattr(skillTab, temp, 5)
            db.session.add(skillTab)
            db.session.flush()
            majorSkills = db.session.query(Skill).filter_by(id=skillTab.id).first()
            degree = Degree()
            degree.name = major.find('title').text
            degree.description = major.find('description').text
            degree.id = majorSkills.id
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
        checkExist = db.session.query(SkillNames).filter_by(name=skill.text).first()
        if checkExist is None:
            skillName = SkillNames()
            skillName.name = skill.text
            db.session.add(skillName)
            db.session.commit()
    return


def getSkillData(id):
    resultDict = {}
    skillNames = db.session.query(SkillNames).all()
    skill = db.session.query(Skill).filter_by(id=id).first()
    for skillName in skillNames:
        resultName = skillName.name.replace(' ', '_')
        resultName = resultName.replace('/', '_')
        resultName = resultName.replace('+', 'p')
        resultName = resultName.lower()
        # CAN REMOVE TRY BLOCK IF DATABASE AND XML BECOME FULLY SYNCED
        try:
            resultDict[resultName] = getattr(skill, resultName)
        except AttributeError:
            resultDict[resultName] = 0
    return resultDict

def getAllJobs():
    resultDict = {}
    jobs = db.session.query(Job).all()
    for job in jobs:
        jobSkill = getSkillData(job.id)
        resultDict[job.name] = jobSkill
    return resultDict


def getAllDegrees():
    resultDict = {}
    degrees = db.session.query(Degree).all()
    for degree in degrees:
        degreeSkill = getSkillData(degree.id)
        resultDict[degree.name] = degreeSkill
    return resultDict

def search_by_degree(user, degree):
    user_skills = getSkillData(user.get_skill_id())
    degree_skills = getSkillData(degree.get_id())
    combined_skills = {}
    for k in user_skills.iterkeys():
        combined_skills[k] = user_skills[k] + degree_skills[k]
        if combined_skills[k] > 5:
            combined_skills[k] = 5
    jobs = getAllJobs()
    resultDict = {}
    for job in jobs.iterkeys():
        job_skills = jobs[job]
        skill_num = 0.00
        resultDict[job] = 0.00
        for skill in job_skills.iterkeys():
            skill_num += 1.00
            if combined_skills[skill] >= job_skills[skill]:
                resultDict[job] += 100.00
            else:
                resultDict[job] += ((combined_skills[skill]*1.00) / job_skills[skill]) * 100.00
        resultDict[job] = float('%.2f'%(resultDict[job] / skill_num))
    search = Search()
    search.user_id = user.get_id()
    search.using = degree.get_name()
    user.recent_search = ';'.join(str(t) for t in (sort_results(resultDict)))
    db.session.add(search)
    db.session.commit()
    return resultDict


def search_by_job(user, job):
    user_skills = getSkillData(user.get_skill_id())
    job_skills = getSkillData(job.get_id())
    missing_skills = {}
    for k in user_skills.iterkeys():
        missing_skills[k] = job_skills[k] - user_skills[k]
        if missing_skills[k] < 0:
            missing_skills[k] = 0
    degrees = getAllDegrees()
    resultDict = {}
    for degree in degrees.iterkeys():
        degree_skills = degrees[degree]
        skill_num = 0.00
        resultDict[degree] = 0
        for skill in degree_skills.iterkeys():
            if missing_skills[skill] != 0:
                skill_num += 1.00
                if degree_skills[skill] >= missing_skills[skill]:
                    resultDict[degree] += 100.00
                else:
                    resultDict[degree] += ((degree_skills[skill]*1.00) / missing_skills[skill]) * 100.00
        resultDict[degree] = float('%.2f'%(resultDict[degree] / skill_num))
    search = Search()
    search.user_id = user.get_id()
    search.using = job.get_name()
    user.recent_search = ';'.join(str(t) for t in (sort_results(resultDict)))
    db.session.add(search)
    db.session.commit()
    return missing_skills

def sort_results(resultDict):
    l = list()
    for key in resultDict.iterkeys():
        l.append((key, resultDict[key]))
    return sorted(l, key=lambda entry: entry[1], reverse=True)

def get_search_params(user_id):
    q = db.session.query(db.func.max(Search.search_number)).\
        join(Search.user).\
        filter(User.id==user_id).all()
    search = db.session.query(Search).get(q[0][0])
    return search.using

def get_search_history():
    return db.session.query(Search.using, db.func.count(Search.using)).group_by(Search.using).all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

