
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db=SQLAlchemy()
DB_NAME = "log.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    db.init_app(app)
          
    import views
    import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from models import User,Posts,Comments,Like,Follow
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'   #redirect to login page if not logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))   #get user from database 

    return app
    
def create_db(app):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print("Database created")
    