from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# Keep this config file for these two informations
from .config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


def create_app():
    app = Flask(__name__)

    db = SQLAlchemy(app)

    app.config['SECRET_KEY'] = SECRET_KEY
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    from .models import Users, Notes

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app
