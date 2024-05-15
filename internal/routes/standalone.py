import os, io
import flask, werkzeug
import database
from misc import shared, session





@shared.app.route('/', methods = ['GET'])
def index():
    user_id = session.check()
    user_name = None
    user_surname = None
    if user_id:
        user_name = database.user.name_read(user_id)
        user_surname = database.user.surname_read(user_id)
    return flask.render_template('standalone/index.html', user_id = user_id, user_name = user_name, user_surname = user_surname)

#@shared.app.errorhandler(werkzeug.exceptions.HTTPException)
#def error_handler(error):
#    return flask.render_template('error.html', error = error, error_index = error.code), error.code





@shared.app.route('/project/<project_id>', methods = ['GET'])
def project(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    project_user_id = database.project.user_read(project_id)
    project_user_name = database.user.name_read(project_user_id)
    project_user_surname = database.user.surname_read(project_user_id)
    project_date = database.project.date_read(project_id)
    project_name = database.project.name_read(project_id)
    project_type = database.project.type_read(project_id)
    project_original = database.project.original_read(project_id)
    project_translation = database.project.translation_read(project_id)
    project_description = database.project.description_read(project_id)
    
    project_previews = []
    for l in range(database.project.previews_count(project_id)):
        project_previews.append(database.project.previews_read(project_id, l))

    user_id = session.check()
    user_name = None
    user_surname = None
    if user_id:
        user_name = database.user.name_read(user_id)
        user_surname = database.user.surname_read(user_id)
    return flask.render_template('standalone/project.html', user_id = user_id, user_name = user_name, user_surname = user_surname, project_id = project_id,
                                    project_user_id = project_user_id, project_user_name = project_user_name, project_user_surname = project_user_surname,
                                    project_date = project_date, project_name = project_name, project_type = project_type, project_original = project_original,
                                    project_translation = project_translation, project_description = project_description, project_previews = project_previews)

@shared.app.route('/project/<project_id>/thumbnail', methods = ['GET'])
def project_thumbnail(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    thumbnail = database.project.thumbnail_read(project_id)
    thumbnail.seek(0, os.SEEK_END)
    if thumbnail.tell() < 10:
        flask.abort(404)
        with open(os.path.join(os.getcwd(), 'internal', 'static', 'project-default.png'), 'rb') as file:
            thumbnail = io.BytesIO(file.read())
    else:
        thumbnail.seek(0)
    return flask.send_file(thumbnail, mimetype = 'image/jpeg')

@shared.app.route('/project/<project_id>/content', methods = ['GET'])
def project_content(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    content = database.project.content_read(project_id)
    content.seek(0, os.SEEK_END)
    if content.tell() < 10:
        flask.abort(404)
    
    content.seek(0)
    return flask.send_file(content, mimetype = 'application/pdf')

@shared.app.route('/project/<project_id>/update', methods = ['POST'])
def project_update(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    if database.project.user_read(project_id) != session.check() or not set(('name', 'type', 'original', 'translation', 'description')).issubset(flask.request.form):
        flask.abort(401)
    database.project.name_update(project_id, flask.request.form['name'])
    database.project.type_update(project_id, flask.request.form['type'])
    database.project.original_update(project_id, flask.request.form['original'])
    database.project.translation_update(project_id, flask.request.form['translation'])
    database.project.description_update(project_id, flask.request.form['description'])
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/project/<project_id>/newthumbnail', methods = ['POST'])
def project_new_thumbnail(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    if database.project.user_read(project_id) != session.check() or ('thumbnail' not in flask.request.files):
        flask.abort(401)

    thumbnail = flask.request.files['thumbnail']
    if not thumbnail.filename:
        return flask.jsonify({'result': 'empty'})

    database.project.thumbnail_update(project_id, thumbnail)
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/project/<project_id>/newcontent', methods = ['POST'])
def project_new_content(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    if database.project.user_read(project_id) != session.check() or ('content' not in flask.request.files):
        flask.abort(401)

    content = flask.request.files['content']
    if not content.filename:
        return flask.jsonify({'result': 'empty'})

    database.project.content_update(project_id, content)
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/project/<project_id>/addpreview', methods = ['POST'])
def project_add_preview(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    if database.project.user_read(project_id) != session.check() or not set(('original', 'translation')).issubset(flask.request.form):
        flask.abort(401)

    database.project.previews_write(project_id, flask.request.form['original'], flask.request.form['translation'])
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/project/<project_id>/removepreview', methods = ['POST'])
def project_remove_preview(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    if database.project.user_read(project_id) != session.check() or ('index' not in flask.request.form):
        flask.abort(401)
    index = int(flask.request.form['index'])

    if database.project.previews_count(project_id) <= index:
        return flask.jsonify({'result': 'invalid'})

    database.project.previews_delete(project_id, index)
    return flask.jsonify({'result': 'ok'})

@shared.app.route('/project/<project_id>/updatepreview', methods = ['POST'])
def project_update_preview(project_id):
    if not database.project.exists(project_id):
        flask.abort(404)
    if database.project.user_read(project_id) != session.check() or not set(('index', 'original', 'translation')).issubset(flask.request.form):
        flask.abort(401)
    index = int(flask.request.form['index'])

    if database.project.previews_count(project_id) <= index:
        return flask.jsonify({'result': 'invalid'})

    database.project.previews_update(project_id, index, flask.request.form['original'], flask.request.form['translation'])
    return flask.jsonify({'result': 'ok'})