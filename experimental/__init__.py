import os, base64
import flask, flask_sqlalchemy, flask_migrate, sqlalchemy

application = flask.Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.getcwd(), "experimental", "database", "db.sqlite")}'

database = flask_sqlalchemy.SQLAlchemy()
database.init_app(application)

def generate_new_id():
    return str(base64.urlsafe_b64encode(os.urandom(6)), 'ascii')

mapped_column = sqlalchemy.orm.mapped_column
relationship = sqlalchemy.orm.relationship
class user_model(database.Model):
    id         = mapped_column(sqlalchemy.Text,
                               primary_key = True,
                               default = generate_new_id)
    name       = mapped_column(sqlalchemy.UnicodeText,
                               nullable = False)
    surname    = mapped_column(sqlalchemy.UnicodeText,
                               nullable = False)
    languages  = mapped_column(sqlalchemy.JSON,
                               nullable = False,
                               default = [])
    projects   = relationship('project_model',
                               back_populates = 'user',
                               cascade = 'all, delete-orphan',
                               uselist = True)
    avatar_ref = mapped_column(sqlalchemy.ForeignKey('file_model.id'))
    avatar     = relationship('file_model',
                               foreign_keys = avatar_ref,
                               cascade = 'all, delete-orphan',
                               uselist = False,
                               single_parent = True) 

class project_model(database.Model):
    id       = mapped_column(sqlalchemy.Text,
                             primary_key = True,
                             default = generate_new_id)
    name     = mapped_column(sqlalchemy.UnicodeText,
                             nullable = False)
    user_ref = mapped_column(sqlalchemy.ForeignKey('user_model.id'),
                             nullable = False)
    user     = relationship('user_model',
                             back_populates = 'projects',
                             foreign_keys = user_ref,
                             uselist = False)

class file_model(database.Model):
    id       = mapped_column(sqlalchemy.Text,
                             primary_key = True,
                             default = generate_new_id)
    contents = mapped_column(sqlalchemy.LargeBinary,
                             nullable = False)

migrate = flask_migrate.Migrate(application, database)

@application.get('/')
def index():
    database.session.add(user_model(name = 'A', surname = 'a'))
    database.session.commit()
    return flask.render_template('index.html', users = user_model.query.all())

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