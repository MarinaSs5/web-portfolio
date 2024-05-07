import sys, os, time, io
import flask
sys.path.append(os.path.join(os.getcwd(), 'internal'))
sys.path.append(os.path.join(os.getcwd(), 'internal', '*'))
from misc import shared





shared.app = flask.Flask(__name__)
from misc import mail
import database, routes

shared.app.secret_key = 'secret'
shared.app.permanent_session_lifetime = 60 * 60 * 24 * 30
database.start()

@shared.app.route('/save', methods = ['GET'])
def save():
    database.save()
    return flask.redirect('/', code = 307)





if __name__ == '__main__':
    try:
        shared.app.run(host = 'localhost', port = 8000)
    finally:
        database.save()
else:
    app = shared.app