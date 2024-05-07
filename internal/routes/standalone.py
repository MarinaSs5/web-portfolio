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