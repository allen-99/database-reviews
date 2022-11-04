from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate.init_app(app, db)

    from review.models.models import Text, Theme, BlockOfText, Company, Platform
    from review.routes.auth import User

    from review.routes.routes import main as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from review.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app
