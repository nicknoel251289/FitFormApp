from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# 1. This tells flask how we log in/find a user
# 2. Helps us manage all the logged in things
from flask_login import LoginManager

# 1. initialize DB
db = SQLAlchemy()
DB_NAME = "database.db"

# 1. initialize flask
def create_app():
    app = Flask(__name__)
    # 1. encrypt and store session data related to our website. Don't share this key
    app.config['SECRET_KET'] = 'r4564566456'
    app.secret_key = b'awd32424ase'

    # 1. Where the DB location is storred at
    # 2. The f allows us to use '{}' brackets and python code; it gets evaluated as a string
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # 1. Where our endpoints are in our app. We import the name of the blueprint variable using the 
    #    relative path by denoting the '.'
    from .views import views
    from .auth import auth
    from .exercise_list_page import exercise_list_page
    from .exercises import exercises

    # 1. This just adds a prefix to the URL/route if we defined one specifically in the blueprint. As an
    #    example, if our auth blueprint use @auth.route('/auth') and we also defined a prefix here, it would
    #    be appended to the '/auth'.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(exercise_list_page, url_prefix='/')
    app.register_blueprint(exercises, url_prefix='/')

    # 1. We must import .model (file name) because we need to make sure that we load this file and load define
    #    the classes in the file, before we initialize or crete or DB.
    # 2. 
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    # 1. Where will flask redirect us if we are not logged in and a login is required
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # 1. This tells flask how to load a user; essentially what user to look for based off of ID(primary key)
    # 2. User.query.get() by default will look for the primary key and check if it is equal to whatever we pass
    #    it, which is the int version of whatever is passed as the argument to load_user 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# 1. db.create_all takes the argument that tells flask SQL which app we are creating the DB for.
# 2. The app also has the SQL alchemy database URI on it which tells us where to create the DB
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created DB')