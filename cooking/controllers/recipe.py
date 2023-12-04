import datetime
import dateutil.tz
from sqlalchemy import func
from flask import Blueprint, render_template, request, url_for, redirect
import flask_login
from flask_login import current_user
from . import model
from .. import db

bp = Blueprint("recipe", __name__)

@bp.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):

    recipe = db.get_or_404(model.Recipe, recipe_id)

    rating_value = db.session.query(func.avg(model.Rating.rating)).where(model.Rating.recipe_id == recipe.id).scalar()
    rating_value = round(rating_value * 2) / 2

    return render_template("main/recipe.html", recipe=recipe, rating_value=rating_value)


@bp.route("/new_rating", methods=["POST"])
def new_rating():
    comment = request.form.get("text")
    stars = request.form.get("stars")
    recipe_id = request.form.get("recipe_id")


    rating = model.Rating(
        rating=stars,
        recipe_id=recipe_id,
        user_id=1,
        comment=comment
    )
    

    db.session.add(rating)
    db.session.commit()

    return redirect(url_for("recipe.recipe", recipe_id = recipe_id))



