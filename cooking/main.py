import datetime
import dateutil.tz

from flask import Blueprint, render_template


from . import model

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
    recipes = [Recipe("Chicken Parmesan", "A delicious chicken dish", 4, 60),
               Recipe("Pasta Carbonara", "A delicious pasta dish", 2, 30),
               Recipe("Steak", "A delicious steak", 1, 15),
               Recipe("Fish", "A delicious fish", 1, 20),
               Recipe("Burger", "A delicious burger", 1, 20),
               Recipe("Pizza", "A delicious pizza", 1, 20),
               Recipe("Chicken", "A delicious chicken", 1, 20),
               Recipe("Pasta", "A delicious pasta", 1, 20),
               Recipe("Salad", "A delicious salad", 1, 20),
               Recipe("Soup", "A delicious soup", 1, 20),
               Recipe("Sandwich", "A delicious sandwich", 1, 20)]
    return render_template("main/index.html", recipes=recipes)

@bp.route("/profile")
def profile():
    return render_template("main/profile.html")

@bp.route("/create")
@flask_login.login_required
def create():
    return render_template("main/create_recipe.html")
