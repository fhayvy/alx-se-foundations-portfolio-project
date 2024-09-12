from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
DB_NAME = 'barelybare.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ggfhjhgfjghijljk*&^%$hhjkjhj%bxbcnvbm,#@$%^&**&'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate.init_app(app,db)

    from .views import products
    from .users import users

    # Register the Blueprints
    app.register_blueprint(products, url_prefix='/')
    app.register_blueprint(users, url_prefix='/users')

    from . import models


    # create_database(app)
    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')