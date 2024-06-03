import time, functools
import flask, sqlalchemy
import database as db, authentication as auth





def clear():
    [flask.session.pop(key) for key in list(flask.session.keys())]

def fetch_from_session(**kw):
    required = kw.get('required', False)
    redirect_unwanted_to = kw.get('redirect_unwanted_to', None)
    output_kw = kw.get('output_kw', 'user')

    def w(f):
        @functools.wraps(f)
        def ww(*args, **kwargs):

            instance = None
            if ('0' in flask.session) and ('1' in flask.session) and ('2' in flask.session):
                potential = db.execute(db.handle.select(db.models.user.sessions, db.models.user.auth).where(db.models.user.id == flask.session['0'])).first()
                auth1 = flask.session['1']
                auth2 = flask.session['2']
                if potential:
                    for sess in potential.sessions:
                        session_details = auth.check_session(sess[0], sess[1], auth1, auth2)
                        if session_details:
                            if auth.check_auth(potential.auth, session_details[0]) and (session_details[1] == flask.request.remote_addr + flask.request.user_agent.string):
                                instance = db.execute(db.handle.select(db.models.user).where(db.models.user.id == flask.session['0'])).scalar()
                                break
 
            if required and (not instance):
                clear()
                flask.abort(401)
            if redirect_unwanted_to and instance:
                return flask.redirect(redirect_unwanted_to, code = 307)
            kwargs[output_kw] = instance
        
            return f(*args, **kwargs)
        return ww
    return w

# assign new session (signin / signup)
def assign(user, password):
    session_details = auth.generate_session(password, flask.request.remote_addr + flask.request.user_agent.string, 60 * 40 * 24 * 30)
    user.sessions.append([session_details[0], session_details[1]])
    clear()
    flask.session.permanent = True
    flask.session['0'] = user.id
    flask.session['1'] = session_details[2]
    flask.session['2'] = session_details[3]
    sqlalchemy.orm.attributes.flag_modified(user, 'sessions')





def assssssssssssssssssign(user_id, user_password, verify):
    if verify:
        if not database.user.exists(user_id):
            return False
        if not authentication.check_existing_auth(database.user.auth_read(user_id), user_password):
            return False

    session_details = authentication.generate_new_session(user_id, user_password, flask.request.remote_addr + flask.request.user_agent.string, 60 * 60 * 24 * 30)
    database.user.sessions_write(user_id, session_details[0], session_details[1])
    clear()
    flask.session.permanent = True
    flask.session['0'] = user_id
    flask.session['1'] = session_details[2]
    flask.session['2'] = session_details[3]
    return True

def check():
    if (not '0' in flask.session) or (not '1' in flask.session) or (not '2' in flask.session):
        #clear()
        return None

    user_id = flask.session['0']
    if not database.user.exists(user_id):
        #clear()
        return None
    
    user_sessions = []
    for s in range(database.user.sessions_count(user_id)):
        user_sessions.append(database.user.sessions_read(user_id, s))
    offset = 0
    for s in range(len(user_sessions)):
        if user_sessions[s - offset][1] < time.time():
            del user_sessions[s - offset]
            database.user.sessions_delete(user_id, s - offset)
            offset += 1
    if not user_sessions:
        #clear()
        return None

    once_valid = False
    for session in user_sessions:
        session_details = authentication.check_existing_session(session[0], session[1], flask.session['1'], flask.session['2'])
        if session_details:
            if authentication.check_existing_auth(database.user.auth_read(user_id), session_details[0]) and\
                    session_details[1] == flask.request.remote_addr + flask.request.user_agent.string:
                once_valid = True
                break
    if not once_valid:
        #clear()
        return None
    

    return user_id    