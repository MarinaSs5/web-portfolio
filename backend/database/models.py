import sqlalchemy
import database as db





class user(db.handle.Model):
    id         = db.explicit_key(sqlalchemy.Text)
    auth       = db.protected_required_field(sqlalchemy.Text)
    sessions   = db.protected_array_field()
    name       = db.required_field(sqlalchemy.UnicodeText)
    surname    = db.required_field(sqlalchemy.UnicodeText)
    specialty  = db.optional_field(sqlalchemy.UnicodeText)
    job        = db.optional_field(sqlalchemy.UnicodeText)
    mail       = db.optional_field(sqlalchemy.UnicodeText)
    vk         = db.optional_field(sqlalchemy.UnicodeText)
    tg         = db.optional_field(sqlalchemy.UnicodeText)
    city       = db.optional_field(sqlalchemy.UnicodeText)
    languages  = db.array_field()
    avatar_ref = db.optional_reference('file.id')
    avatar     = sqlalchemy.orm.relationship('file', foreign_keys = avatar_ref, cascade = 'all, delete-orphan', uselist = False, single_parent = True, lazy = 'raise') # one-to-one fore, yes foreref, no backref
    about      = db.optional_field(sqlalchemy.UnicodeText)
    skill      = db.optional_field(sqlalchemy.UnicodeText)
    projects   = sqlalchemy.orm.relationship('project', back_populates = 'user', cascade = 'all, delete-orphan', uselist = True, lazy = 'raise') # one-to-many fore, no foreref, yes backref

class project(db.handle.Model):
    id          = db.implicit_key()
    user_ref    = db.required_reference('user.id')
    user        = sqlalchemy.orm.relationship('user', back_populates = 'projects', foreign_keys = user_ref, uselist = False, lazy = 'raise') # one-to-many back, no foreref, yes backref
    date        = db.required_field(sqlalchemy.Double)
    name        = db.required_field(sqlalchemy.UnicodeText)
    type        = db.optional_field(sqlalchemy.UnicodeText)
    original    = db.optional_field(sqlalchemy.UnicodeText)
    translation = db.optional_field(sqlalchemy.UnicodeText)
    description = db.optional_field(sqlalchemy.UnicodeText)
    thumbnail_ref       = db.optional_reference('file.id')
    thumbnail           = sqlalchemy.orm.relationship('file', foreign_keys = thumbnail_ref, cascade = 'all, delete-orphan', uselist = False, single_parent = True, lazy = 'raise') # one-to-one fore, yes foreref, no backref
    content_ref         = db.optional_reference('file.id')
    content             = sqlalchemy.orm.relationship('file', foreign_keys = content_ref, cascade = 'all, delete-orphan', uselist = False, single_parent = True, lazy = 'raise') # one-to-one fore, yes foreref, no backref
    preview_original    = db.optional_field(sqlalchemy.UnicodeText)
    preview_translation = db.optional_field(sqlalchemy.UnicodeText)

class file(db.handle.Model):
    id       = db.implicit_key()
    contents = db.required_field(sqlalchemy.LargeBinary)