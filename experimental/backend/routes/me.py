import io, time
import flask, sqlalchemy
import database as db, application as app, session, decorators





@app.get('/me/<user>/info')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile')
@session.fetch_from_session(output_kw = 'user')
def me_info(profile, user):
    return flask.render_template('me/info.html', user = user, profile = profile)

@app.post('/me/<user>/info/update')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile')
@session.fetch_from_session(output_kw = 'user', required = True)
@decorators.keywordize_post_arguments('name', 'surname', 'specialty', 'city', 'job', 'mail', 'vk', 'tg', 'about', 'skill', required = True)
@db.save_changes
def me_info_update(profile, user, name, surname, specialty, city, job, mail, vk, tg, about, skill):
    if profile != user: 
        flask.abort(401)

    profile.name = name
    profile.surname = surname
    profile.specialty = specialty
    profile.city = city
    profile.job = job
    profile.mail = mail
    profile.vk = vk
    profile.tg = tg
    profile.about = about
    profile.skill = skill
    return flask.jsonify({'result': 'ok'})

@app.post('/me/<user>/info/addlanguage')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile')
@session.fetch_from_session(output_kw = 'user', required = True)
@decorators.keywordize_post_arguments('language', 'level', required = True)
@db.save_changes
def info_add_lang(profile, user, language, level):
    if profile != user: 
        flask.abort(401)
    profile.languages.append([language, level])
    sqlalchemy.orm.attributes.flag_modified(profile, 'languages')
    return flask.jsonify({'result': 'ok'})

@app.post('/me/<user>/info/removelanguage')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile')
@session.fetch_from_session(output_kw = 'user', required = True)
@decorators.keywordize_post_arguments('index', required = True)
@db.save_changes
def info_r_lang(profile, user, index):
    if profile != user: 
        flask.abort(401)
    index = int(index)
    if index < len(profile.languages):
        del profile.languages[index]
    sqlalchemy.orm.attributes.flag_modified(profile, 'languages')
    return flask.jsonify({'result': 'ok'})

@app.post('/me/<user>/info/newavatar')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile', query_options = (db.allow(db.models.user.avatar),))
@session.fetch_from_session(output_kw = 'user', required = True)
@db.save_changes
def info_a(profile, user):
    if profile != user or ('avatar' not in flask.request.files):
        flask.abort(401)

    avatar = flask.request.files['avatar']
    if not avatar.filename:
        return flask.jsonify({'result': 'empty'})
    
    profile.avatar = db.models.file(contents = avatar.read())
    return flask.jsonify({'result': 'ok'})









@app.get('/me/<user>/avatar')
@db.fetch_from_keyword(db.models.user, query_options = (db.allow(db.models.user.avatar),))
def av(user):
    if not user.avatar_ref:
        flask.abort(404)
    
    return flask.send_file(io.BytesIO(user.avatar.contents), mimetype = 'image/jpeg')











@app.get('/me/<user>/projects')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile', query_options = (db.allow(db.models.user.projects),))
@session.fetch_from_session(output_kw = 'user')
def proj(user, profile):
    return flask.render_template('me/projects.html', user = user, profile = profile)

@app.post('/me/<user>/projects/add')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile', query_options = (db.allow(db.models.user.projects),))
@session.fetch_from_session(output_kw = 'user', required = True)
@decorators.keywordize_post_arguments('name', required = True)
def pr_add(profile, user, name):
    if profile != user: 
        flask.abort(401)

    pr = db.models.project(user = profile, name = name, date = time.time())
    profile.projects.append(pr)
    db.handle.session.commit()
    return flask.jsonify({'result': pr.id})

@app.post('/me/<user>/projects/remove')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile', query_options = (db.allow(db.models.user.projects),))
@session.fetch_from_session(output_kw = 'user', required = True)
@decorators.keywordize_post_arguments('id', required = True)
@db.save_changes
def pr_ad(profile, user, id):
    if profile != user: 
        flask.abort(401)

    for pr in range(len(profile.projects)):
        if profile.projects[pr].id == id:
            del profile.projects[pr]
            break
    return flask.jsonify({'result': 'ok'})