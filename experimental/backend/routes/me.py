import flask
import database as db, application as app, session





@app.get('/me/<user>/info')
@db.fetch_from_keyword(db.models.user, output_kw = 'profile')
@session.fetch_from_session(output_kw = 'user')
def me_info(profile, user):
    return flask.render_template('me/info.html', user = user, profile = profile)