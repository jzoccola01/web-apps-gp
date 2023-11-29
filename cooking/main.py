import datetime
import dateutil.tz

from flask import Blueprint, render_template


from . import model

from . import db

import flask_login

bp = Blueprint("main", __name__)



# For testing before recipe creation implemented

class Recipe:
    def __init__(self, title, description, servings, cook_time, photo="static/logo.png"):
        self.title = title
        self.description = description
        self.servings = servings
        self.cook_time = cook_time
        self.photo = photo



@bp.route("/")
def index():
    query = db.select(model.Recipe)
    recipes = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes)

@bp.route("/profile")
def profile():
    return render_template("main/profile.html")

@bp.route("/create")
@flask_login.login_required
def create():
    return render_template("main/create_recipe.html")
