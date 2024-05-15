import os, io, time
import flask
import database
from misc import shared, session





@shared.app.route('/me/<profile_id>/info', methods = ['GET'])
def info(profile_id):
    if not database.user.exists(profile_id):
        flask.abort(404)
    profile_name = database.user.name_read(profile_id)
    profile_surname = database.user.surname_read(profile_id)
    profile_specialty = database.user.specialty_read(profile_id)
    profile_languages = []
    for l in range(database.user.languages_count(profile_id)):
        profile_languages.append(database.user.languages_read(profile_id, l))
    profile_job = database.user.job_read(profile_id)
    profile_mail = database.user.mail_read(profile_id)
    profile_vk = database.user.vk_read(profile_id)
    profile_tg = database.user.tg_read(profile_id)
    profile_city = database.user.city_read(profile_id)
    profile_about = database.user.about_read(profile_id)
    profile_skill = database.user.skill_read(profile_id)

    user_id = session.check()
    user_name = None
    user_surname = None
    if user_id:
        user_name = database.user.name_read(user_id)
        user_surname = database.user.surname_read(user_id)
    
    return flask.render_template('me/info.html', user_id = user_id, user_name = user_name, user_surname = user_surname,
            profile_id = profile_id, profile_name = profile_name, profile_surname = profile_surname,
            profile_specialty = profile_specialty, profile_languages = profile_languages, profile_job = profile_job,
            profile_mail = profile_mail, profile_vk = profile_vk, profile_tg = profile_tg, profile_city = profile_city,
            profile_about = profile_about, profile_skill = profile_skill)

@shared.app.route('/me/<profile_id>/info/update', methods = ['POST'])
def info_update(profile_id):
    if profile_id != session.check() or not all([(field in flask.request.form) for field in ('name', 'surname', 'specialty', 'city', 'job', 'mail', 'vk', 'tg', 'about', 'skill')]):
        flask.abort(401)

    database.user.name_update(profile_id, flask.request.form['name'])
    database.user.surname_update(profile_id, flask.request.form['surname'])
    database.user.specialty_update(profile_id, flask.request.form['specialty'])
    database.user.job_update(profile_id, flask.request.form['job'])
    database.user.mail_update(profile_id, flask.request.form['mail'])
    database.user.vk_update(profile_id, flask.request.form['vk'])
    database.user.tg_update(profile_id, flask.request.form['tg'])
    database.user.city_update(profile_id, flask.request.form['city'])
    database.user.about_update(profile_id, flask.request.form['about'])
    database.user.skill_update(profile_id, flask.request.form['skill'])
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/me/<profile_id>/info/addlanguage', methods = ['POST'])
def info_add_language(profile_id):
    if profile_id != session.check() or not all([(field in flask.request.form) for field in ('language', 'level')]):
        flask.abort(401)

    database.user.languages_write(profile_id, flask.request.form['language'], flask.request.form['level'])
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/me/<profile_id>/info/removelanguage', methods = ['POST'])
def info_remove_language(profile_id):
    if profile_id != session.check() or ('index' not in flask.request.form):
        flask.abort(401)
    index = int(flask.request.form['index'])

    if database.user.languages_count(profile_id) <= index:
        return flask.jsonify({'result': 'invalid'})

    database.user.languages_delete(profile_id, index)
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/me/<profile_id>/info/newavatar', methods = ['POST'])
def info_new_avatar(profile_id):
    if profile_id != session.check() or ('avatar' not in flask.request.files):
        flask.abort(401)

    avatar = flask.request.files['avatar']
    if not avatar.filename:
        return flask.jsonify({'result': 'empty'})

    database.user.avatar_update(profile_id, avatar)
    return flask.jsonify({'result': 'ok'})





@shared.app.route('/me/<profile_id>/avatar', methods = ['GET'])
def avatar(profile_id):
    if not database.user.exists(profile_id):
        flask.abort(404)
    avatar = database.user.avatar_read(profile_id)
    avatar.seek(0, os.SEEK_END)
    if avatar.tell() < 10:
        flask.abort(404)
        with open(os.path.join(os.getcwd(), 'internal', 'static', 'profile-photo.png'), 'rb') as file:
            avatar = io.BytesIO(file.read())
    else:
        avatar.seek(0)
    return flask.send_file(avatar, mimetype = 'image/jpeg')





@shared.app.route('/me/<profile_id>/projects', methods = ['GET'])
def projects(profile_id):
    if not database.user.exists(profile_id):
        flask.abort(404)
    profile_name = database.user.name_read(profile_id)
    profile_surname = database.user.surname_read(profile_id)
    profile_projects = []
    for l in range(database.user.projects_count(profile_id)):
        pr_id = database.user.projects_read(profile_id, l)[0]
        profile_projects.append((pr_id, database.project.name_read(pr_id)))

    user_id = session.check()
    user_name = None
    user_surname = None
    if user_id:
        user_name = database.user.name_read(user_id)
        user_surname = database.user.surname_read(user_id)

    return flask.render_template('me/projects.html', user_id = user_id, user_name = user_name, user_surname = user_surname,
            profile_id = profile_id, profile_name = profile_name, profile_surname = profile_surname, profile_projects = profile_projects)

@shared.app.route('/me/<profile_id>/projects/add', methods = ['POST'])
def projects_add(profile_id):
    if profile_id != session.check() or ('name' not in flask.request.form):
        flask.abort(401)
    
    while True:
        pr_id = os.urandom(4).hex()
        if not database.project.exists(pr_id): break

    database.project.create(pr_id, profile_id, time.time(), flask.request.form['name'])
    database.user.projects_write(profile_id, pr_id)
    return flask.jsonify({'result': pr_id})

@shared.app.route('/me/<profile_id>/projects/remove', methods = ['POST'])
def projects_remove(profile_id):
    if profile_id != session.check() or ('id' not in flask.request.form):
        flask.abort(401)

    pr_id = flask.request.form['id']
    if not database.project.exists(pr_id):
        return flask.jsonify({'result': 'invalid'})

    database.project.remove(pr_id)
    for l in range(database.user.projects_count(profile_id)):
        if database.user.projects_read(profile_id, l)[0] == pr_id:
            database.user.projects_delete(profile_id, l)
            break
    return flask.jsonify({'result': 'ok'})