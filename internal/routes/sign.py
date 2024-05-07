import flask
import database
from misc import shared, authentication, session




@shared.app.route('/sign/up', methods = ['GET'])
def signup():
    if session.check():
        return flask.redirect('/', code = 307)
    return flask.render_template('sign/up.html')

@shared.app.route('/sign/up/submit', methods = ['POST'])
def signup_submit():
    if session.check() or not all([(field in flask.request.form) for field in ('login', 'password', 'name', 'surname')]): 
        flask.abort(401)
    
    user_id = flask.request.form['login']
    user_password = flask.request.form['password']
    user_name = flask.request.form['name']
    user_surname = flask.request.form['surname']

    if database.user.exists(user_id):
        return flask.jsonify({'result': 'already'})

    database.user.create(user_id, authentication.generate_new_auth(user_password), user_name, user_surname)
    session.assign(user_id, user_password, False)
    return flask.jsonify({'result': 'ok'})





@shared.app.route('/sign/in', methods = ['GET'])
def signin():
    if session.check():
        return flask.redirect('/', code = 307)
    return flask.render_template('sign/in.html')

@shared.app.route('/sign/in/submit', methods = ['POST'])
def signin_submit():
    if session.check() or (not 'login' in flask.request.form) or (not 'password' in flask.request.form):
        flask.abort(401)
    
    user_id = flask.request.form['login']
    user_password = flask.request.form['password']

    if session.assign(user_id, user_password, True):
        return flask.jsonify({'result': 'ok'})
    else:
        return flask.jsonify({'result': 'invalid'})





@shared.app.route('/sign/out', methods = ['GET'])
def signout():
    session.clear()
    return flask.redirect('/', code = 307)