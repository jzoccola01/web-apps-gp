import datetime
import dateutil.tz
from sqlalchemy import func
from flask import Blueprint, render_template, request, url_for, redirect

from . import model
from .. import db

bp = Blueprint("recipe", __name__)

@bp.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):

    recipe = db.get_or_404(model.Recipe, recipe_id)

    query = db.select(model.QuantifiedIngredient).where(model.QuantifiedIngredient.recipe_id == recipe.id)
    ingredients = db.session.execute(query).scalars().all()

    query = db.select(model.Step).where(model.Step.recipe_id == recipe.id)
    steps = db.session.execute(query).scalars().all()

    query = db.select(model.Rating).where(model.Rating.recipe_id == recipe.id)
    ratings = db.session.execute(query).scalars().all()

    # Alec, I added the missing filter for only the ratings for this recipe
    rating_value = db.session.query(func.avg(model.Rating.rating)).filter(model.Rating.recipe_id == recipe.id).scalar()

    return render_template("main/recipe.html", recipe=recipe, ingredients=ingredients, steps=steps, ratings=ratings, rating_value=rating_value)


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



