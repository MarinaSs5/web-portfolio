import flask
import database as db, application as app, authentication as auth, session





@app.get('/sign/up')
@session.fetch_from_session(redirect_unwanted_to = '/')
def sign_up(user):
    return flask.render_template('sign/up.html')

@app.post('/sign/up/submit')
@db.save_changes
def signup_submit():
    if not set(('login', 'name', 'surname', 'password')).issubset(flask.request.form):
        flask.abort(401)

    user_id = flask.request.form['login']
    user_pw = flask.request.form['password']
    if db.execute(db.handle.select(db.models.user).where(db.models.user.id == user_id)).scalar():
        return flask.jsonify({'result': 'already'})
    
    new_user = db.models.user(id = user_id, auth = auth.generate_auth(user_pw), name = flask.request.form['name'], surname = flask.request.form['surname'], sessions = [])
    session.assign(new_user, user_pw)
    db.handle.session.add(new_user)
    return flask.jsonify({'result': 'ok'})





@app.get('/sign/in')
@session.fetch_from_session(redirect_unwanted_to = '/')
def sign_in(user):
    return flask.render_template('sign/in.html')

@app.post('/sign/in/submit')
@db.save_changes
def sign_in_submit():
    if not set(('login', 'password')).issubset(flask.request.form):
        flask.abort(401)

    user_id = flask.request.form['login']
    user_pw = flask.request.form['password']

    user = db.execute(db.handle.select(db.models.user)
            .options(db.allow(db.models.user.sessions), db.allow(db.models.user.auth))
            .where(db.models.user.id == user_id)).scalar()
    if not user:
        return flask.jsonify({'result': 'invalid'})
    if not auth.check_auth(user.auth, user_pw):
        return flask.jsonify({'result': 'invalid'})
    session.assign(user, user_pw)
    return flask.jsonify({'result': 'ok'})





@app.get('/sign/out')
def sign_out():
    session.clear()
    return flask.redirect('/', code = 307)