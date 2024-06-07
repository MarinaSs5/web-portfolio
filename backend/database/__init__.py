import os
import flask_sqlalchemy, flask_migrate
import application





application.handle.config['SQLALCHEMY_ECHO'] = application.handle.debug
application.handle.config['SQLALCHEMY_DATABASE_URI'] = f'''sqlite:///{
    os.path.join(application.root_path, "backend", "database", "db.sqlite")}'''

handle = flask_sqlalchemy.SQLAlchemy()
handle.init_app(application.handle)





from database.shorthands import *
from . import models

migrate = flask_migrate.Migrate(application.handle, handle, directory =
        os.path.join(application.root_path, 'backend', 'database', 'migrations'))