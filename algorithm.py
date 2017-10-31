
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
