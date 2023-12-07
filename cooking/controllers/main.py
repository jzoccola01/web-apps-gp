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
    # Default display is to order by average rating
    query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.avg(model.Rating.rating).desc())
    recipes = db.session.execute(query).scalars().all()

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort="option1", category="none", search="")


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

    category = request.form.get("category")
    sort_op = request.form.get("sort")
    search = request.form.get("search")

    new_recipes = []
    if sort_op == "option1":
        # Query to order by the average rating of each recipe
        query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.avg(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()

    elif sort_op == "option2":
        # Query to get the number of ratings for each recipe and order by that
        query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.count(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()
    elif sort_op == "option3":
        # Query to order by the timestamp of each recipe
        query = db.select(model.Recipe).order_by(model.Recipe.timestamp.desc())
        new_recipes = db.session.execute(query).scalars().all()

    if search == "":
        recipes = new_recipes
    else:
        recipes = [r for r in new_recipes if search.lower() in r.title.lower() or search.lower() in r.description.lower() or search.lower() in r.category.lower() or search.lower() in r.user.username.lower() or any(search.lower() in i.ingredient.name.lower() for i in r.quantified_ingredients)]

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()

    return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort=sort_op, category=category, search=search)

@bp.route('/sort', methods=["POST"])
def sort():
    sort_op = request.form.get("sort")
    if sort_op == "option1":
        # Query to order by the average rating of each recipe
        query = db.select(model.Recipe).join(model.Rating, isouter=True).group_by(model.Recipe.id).order_by(db.func.avg(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()

    elif sort_op == "option2":
        # Query to get the number of ratings for each recipe and order by that
        query = db.select(model.Recipe).join(model.Rating, isouter=True).group_by(model.Recipe.id).order_by(db.func.count(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()
    elif sort_op == "option3":
        # Query to order by the timestamp of each recipe
        query = db.select(model.Recipe).order_by(model.Recipe.timestamp.desc())
        new_recipes = db.session.execute(query).scalars().all()

    recipes = new_recipes

    category = request.form.get("category")
    search = request.form.get("search")

    if search == "":
        recipes = new_recipes
    else:
        recipes = [r for r in new_recipes if search.lower() in r.title.lower() or search.lower() in r.description.lower() or search.lower() in r.category.lower() or search.lower() in r.user.username.lower() or any(search.lower() in i.ingredient.name.lower() for i in r.quantified_ingredients)]

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort=sort_op, category=category, search=search)

@bp.route("/filter", methods=["POST"])
def filter():
    category = request.form.get("filter")

    sort_op = request.form.get("sort")
    search = request.form.get("search")

    new_recipes = []
    if sort_op == "option1":
        # Query to order by the average rating of each recipe
        query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.avg(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()

    elif sort_op == "option2":
        # Query to get the number of ratings for each recipe and order by that
        query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.count(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()
    elif sort_op == "option3":
        # Query to order by the timestamp of each recipe
        query = db.select(model.Recipe).order_by(model.Recipe.timestamp.desc())
        new_recipes = db.session.execute(query).scalars().all()

    recipes = new_recipes

    if search == "":
        recipes = new_recipes
    else:
        recipes = [r for r in new_recipes if search.lower() in r.title.lower() or search.lower() in r.description.lower() or search.lower() in r.category.lower() or search.lower() in r.user.username.lower() or any(search.lower() in i.ingredient.name.lower() for i in r.quantified_ingredients)]

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()
    return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort=sort_op, category=category, search=search)

@bp.route("/search", methods=["POST"])
def search():
    search = request.form.get("search")
    sort_op = request.form.get("sort")
    category = request.form.get("category")

    new_recipes = []
    if sort_op == "option1":
        # Query to order by the average rating of each recipe
        query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.avg(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()

    elif sort_op == "option2":
        # Query to get the number of ratings for each recipe and order by that
        query = db.select(model.Recipe).join(model.Rating).group_by(model.Recipe.id).order_by(db.func.count(model.Rating.rating).desc())
        new_recipes = db.session.execute(query).scalars().all()
    elif sort_op == "option3":
        # Query to order by the timestamp of each recipe
        query = db.select(model.Recipe).order_by(model.Recipe.timestamp.desc())
        new_recipes = db.session.execute(query).scalars().all()

    recipes = [r for r in new_recipes if search.lower() in r.title.lower() or search.lower() in r.description.lower() or search.lower() in r.category.lower() or search.lower() in r.user.username.lower() or any(search.lower() in i.ingredient.name.lower() for i in r.quantified_ingredients)]

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()

    return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort="option1", category="none", search=search)