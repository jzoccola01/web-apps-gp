import datetime
import dateutil.tz
from sqlalchemy import func
from flask import Blueprint, render_template, request, url_for, redirect

from . import model
from . import db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():

    query = db.select(model.Recipe)
    recipes = db.session.execute(query).scalars().all()

    return render_template("main/index.html", recipes=recipes)


@bp.route("/create")
def create():
    return render_template("main/create_recipe.html")
