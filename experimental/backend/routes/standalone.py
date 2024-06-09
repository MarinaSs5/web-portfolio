import flask, werkzeug, io
import database as db, application as app, session, decorators





@app.get('/')
@session.fetch_from_session()
def index(user):
    return flask.render_template('standalone/index.html', user = user)







@app.errorhandler(werkzeug.exceptions.HTTPException)
def error_handler(error):
    return (flask.render_template('standalone/error.html', code = error.code), error.code)








@app.get('/project/<project>')
@db.fetch_from_keyword(db.models.project, query_options = (db.allow(db.models.project.user),))
@session.fetch_from_session()
def project(project, user):
    return flask.render_template('standalone/project.html', user = user, project = project)

@app.get('/project/<project>/thumbnail')
@db.fetch_from_keyword(db.models.project, query_options = (db.allow(db.models.project.thumbnail),))
def avd(project):
    if not project.thumbnail_ref:
        flask.abort(404)
    
    return flask.send_file(io.BytesIO(project.thumbnail.contents), mimetype = 'image/jpeg')

@app.get('/project/<project>/content')
@db.fetch_from_keyword(db.models.project, query_options = (db.allow(db.models.project.content),))
def davd(project):
    if not project.content_ref:
        flask.abort(404)
    
    return flask.send_file(io.BytesIO(project.content.contents), mimetype = 'application/pdf')




        

@app.post('/project/<project>/update')
@db.fetch_from_keyword(db.models.project, query_options = (db.allow(db.models.project.user),))
@session.fetch_from_session(required = True)
@decorators.keywordize_post_arguments('name', 'type', 'original', 'translation', 'description', 'preview_original', 'preview_translation', required = True)
@db.save_changes
def pr_u(project, user, name, type, original, translation, description, preview_original, preview_translation):
    if project.user != user:
        flask.abort(401)

    project.name = name
    project.type = type
    project.original = original
    project.translation = translation
    project.description = description
    project.preview_original = preview_original
    project.preview_translation = preview_translation
    return flask.jsonify({'result': 'ok'})
    
@app.post('/project/<project>/newthumbnail')
@db.fetch_from_keyword(db.models.project, query_options = (db.allow(db.models.project.user), db.allow(db.models.project.thumbnail)))
@session.fetch_from_session(required = True)
@db.save_changes
def fffinfo_a(project, user):
    if project.user != user or ('thumbnail' not in flask.request.files):
        flask.abort(401)

    thumbnail = flask.request.files['thumbnail']
    if not thumbnail.filename:
        return flask.jsonify({'result': 'empty'})
    
    project.thumbnail = db.models.file(contents = thumbnail.read())
    return flask.jsonify({'result': 'ok'})

@app.post('/project/<project>/newcontent')
@db.fetch_from_keyword(db.models.project, query_options = (db.allow(db.models.project.user), db.allow(db.models.project.content)))
@session.fetch_from_session(required = True)
@db.save_changes
def fffidnfo_a(project, user):
    if project.user != user or ('content' not in flask.request.files):
        flask.abort(401)

    content = flask.request.files['content']
    if not content.filename:
        return flask.jsonify({'result': 'empty'})
    
    project.content = db.models.file(contents = content.read())
    return flask.jsonify({'result': 'ok'})
