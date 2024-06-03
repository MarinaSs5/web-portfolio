import flask
import database as db, application as app





@app.get('/')
def index():
    return flask.render_template('standalone/index.html')