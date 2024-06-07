import os, functools, base64
import flask, sqlalchemy
from sqlalchemy.orm import mapped_column, relationship
import database as db





generate_id = lambda: str(base64.urlsafe_b64encode(os.urandom(6)), 'ascii')
implicit_key = lambda **kwargs: mapped_column(sqlalchemy.Text, primary_key = True, default = db.generate_id, **kwargs)
explicit_key = lambda typee, **kwargs: mapped_column(typee, primary_key = True, **kwargs)

optional_field = lambda typee, **kwargs: mapped_column(typee, **kwargs)
required_field = lambda typee, **kwargs: mapped_column(typee, nullable = False, **kwargs)
defaulted_field = lambda typee, default, **kwargs: mapped_column(typee, nullable = False, default = default, **kwargs)
array_field = lambda **kwargs: defaulted_field(sqlalchemy.JSON, [], **kwargs)

protected_optional_field = lambda typee, **kwargs: optional_field(typee, deferred_raiseload = True, **kwargs)
protected_required_field = lambda typee, **kwargs: required_field(typee, deferred_raiseload = True, **kwargs)
protected_defaulted_field = lambda typee, default, **kwargs: defaulted_field(typee, default, deferred_raiseload = True, **kwargs)
protected_array_field = lambda **kwargs: defaulted_field(sqlalchemy.JSON, [], deferred_raiseload = True, **kwargs)

required_reference = lambda key, **kwargs: mapped_column(sqlalchemy.ForeignKey(key), nullable = False, **kwargs)
optional_reference = lambda key, **kwargs: mapped_column(sqlalchemy.ForeignKey(key), **kwargs)





execute = lambda query: db.handle.session.execute(query)
allow = lambda column: sqlalchemy.orm.selectinload(column) if isinstance(column.property, sqlalchemy.orm.relationships.RelationshipProperty) else sqlalchemy.orm.undefer(column)
forbid = lambda column: sqlalchemy.orm.raiseload(column) if isinstance(column.property, sqlalchemy.orm.relationships.RelationshipProperty) else sqlalchemy.orm.defer(column, raiseload = True)





def save_changes(f):
    @functools.wraps(f)
    def w(*args, **kwargs):
        result = f(*args, **kwargs)
        db.handle.session.commit()
        return result
    return w

def fetch_from_keyword(table, **kw):
    search_column = kw.get('search_column', sqlalchemy.inspection.inspect(table).primary_key[0])
    input_kw = kw.get('input_kw', table.__tablename__)
    output_kw = kw.get('output_kw', input_kw)
    ignore_none = kw.get('ignore_none', False)
    query_options = kw.get('query_options', tuple())

    def w(f):
        @functools.wraps(f)
        def ww(*args, **kwargs):
            
            instance = execute\
            (
                db.handle.select(table)
                        .options(*query_options)
                        .where(search_column == kwargs[input_kw])
            ).scalar()

            if (not ignore_none) and (not instance):
                flask.abort(404)
            del kwargs[input_kw]
            kwargs[output_kw] = instance

            return f(*args, **kwargs)
        return ww
    return w
