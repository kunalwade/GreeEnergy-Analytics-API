from flask import Flask
# from flask_cors import CORS
from flask_migrate import Migrate
from src.app.api import api
from src.app.database import db
from src.app.jwt import jwt
from src.app.api.security import cors
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['JWT_SECRET_KEY'] = 'supersecretjwtkeyneedstobechanged'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

    # CORS(app)
    MIGRATIONS_DIR = "migrations"
    Migrate(app,db, MIGRATIONS_DIR)
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    return app