import flask
import database as db, application as app, session





@app.get('/')
@session.fetch_from_session()
def index(user):
    return flask.render_template('standalone/index.html', user = user)