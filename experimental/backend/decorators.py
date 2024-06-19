import functools
import flask





def keywordize_post_arguments(*arguments, **kw):
    required = kw.get('required', False)
    unsupplied_code = kw.get('unsupplied_code', 401)

    def w(f):
        @functools.wraps(f)
        def ww(*args, **kwargs):

            for arg in arguments:
                if (arg not in flask.request.form) and required:
                    flask.abort(unsupplied_code)
                kwargs[arg] = flask.request.form.get(arg)

            return f(*args, **kwargs)
        return ww
    return w
