import datetime
import dateutil.tz
from sqlalchemy import func
from flask import Blueprint, render_template, request, url_for, redirect

from . import model

from .. import db

import flask_login

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    query = db.select(model.Recipe).order_by(model.Recipe.timestamp.desc())
    recipes = db.session.execute(query).scalars().all()

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks)


@bp.route("/create")
@flask_login.login_required
def create():
    return render_template("main/create_recipe.html")

@bp.route("/bookmark", methods=["POST"])
@flask_login.login_required
def bookmark():
    recipe_id = request.form.get("recipe-id")
    user_id = flask_login.current_user.id
    query = db.select(model.Bookmark).where(model.Bookmark.recipe_id == recipe_id).where(model.Bookmark.user_id == user_id)
    bookmark = db.session.execute(query).scalar_one_or_none()
    if bookmark:
        db.session.delete(bookmark)
    else:
        new_bookmark = model.Bookmark(user_id=user_id, recipe_id=recipe_id)
        db.session.add(new_bookmark)
    db.session.commit()
    return redirect(url_for("main.index"))
