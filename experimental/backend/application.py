import os, sys
import flask





root_path = os.path.join(os.getcwd(), 'experimental')
sys.path.append(os.path.join(root_path, 'backend'))

handle = flask.Flask(__name__, static_folder = os.path.join(root_path, 'frontend', 'static'),
        template_folder = os.path.join(root_path, 'frontend', 'templates'))
handle.secret_key = 'secret'

get = handle.get
post = handle.post
errorhandler = handle.errorhandler





import routes












'''
@application.get('/proj')
def proj():
    usrs = user_model.query.all()
    usr = usrs[int(os.urandom(4).hex(), 16) % len(usrs)]
    usr.projects.append(project_model(id = os.urandom(4).hex(), name = 'Work'))
    database.session.commit()
    return f'{usr.id}:<br><ul>{"".join([f"<li>{proj.id} - {proj.user.id}</li>" for proj in usr.projects])}</ul>'

@application.get('/p/<id>')
def p(id):
    user = user_model.query.get(id)
    if not user: flask.abort(404)
    user.name = 'a'
    database.session.commit()
    return user.name

@application.get('/la/<id>')
def la(id):
    user = user_model.query.get(id)
    if not user: flask.abort(404)
    user.languages[5] = ['h', 'b1']
    sqlalchemy.orm.attributes.flag_modified(user, 'languages')
    database.session.commit()
    return str(user.languages)

@application.get('/av/<id>')
def av(id):
    user = user_model.query.get(id)
    if not user: flask.abort(404)
    user.avatar = file_model(contents = b'axaxaxa')
    database.session.commit()
    return 'ok'

@application.get('/avv/<id>')
def avv(id):
    user = user_model.query.get(id)
    if not user: flask.abort(404)
    user.avatar = None
    database.session.commit()
    return 'ok'
'''