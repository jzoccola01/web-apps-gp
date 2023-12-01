from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from cooking.config import TestingConfig
# inside the config.py file, we have a class called Config that has boolean values that need
# to be toggled depending on if we are testing or developing.

db = SQLAlchemy()
bcrypt = Bcrypt()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(TestingConfig)

    # A secret for signing session cookies
    app.config["SECRET_KEY"] = "93220d9b340cf9a6c39bac99cce7daf220167498f91fa"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cooking.db"

    db.init_app(app)

    # Register blueprints
    # (we import main from here to avoid circular imports in the next lab)
    from .controllers import main
    from .controllers import auth
    from .controllers import recipe_creation
    from .controllers import profile
    from .controllers import recipe

    login_manager = LoginManager()
    login_manager.login_view = 'main.index'
    login_manager.init_app(app)
    from .controllers import model

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(model.User, int(user_id))

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(recipe_creation.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(recipe.bp)
    return app
