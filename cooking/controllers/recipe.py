import datetime
import dateutil.tz
from sqlalchemy import func
from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
import flask_login
from flask_login import current_user
from . import model
from .. import db

import pathlib
from flask import current_app

bp = Blueprint("recipe", __name__)

@bp.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):

    recipe = db.get_or_404(model.Recipe, recipe_id)

    # Query for average of reviews out of 5 stars for specific recipe
    rating_value = db.session.query(func.avg(model.Rating.rating)).where(model.Rating.recipe_id == recipe.id).scalar()
    if (type(rating_value) == float):
        rating_value = round(rating_value * 2) / 2
    else:
        rating_value = "Not Yet Rated"


    # check if user has already submitted a review
    if current_user.is_authenticated:
        query = db.select(model.Rating).where(model.Rating.user_id == current_user.id).where(model.Rating.recipe_id == recipe_id)
        previous = db.session.execute(query).scalars().all()
        if(len(previous) == 0):
            previously_rated = 0
        else:
            previously_rated = 1
    else:
        previously_rated = 0

    return render_template("main/recipe.html", recipe=recipe, rating_value=rating_value, previously_rated=previously_rated)


@bp.route("/new_rating", methods=["POST"])
def new_rating():
    comment = request.form.get("text")
    stars = request.form.get("stars")
    recipe_id = request.form.get("recipe_id")

    # check if user has already reviewed (should never get called)
    query = db.select(model.Rating).where(model.Rating.user_id == current_user.id).where(model.Rating.recipe_id == recipe_id)
    previous = db.session.execute(query).scalars().all()
    if(len(previous) != 0):
        abort(400, "You have already reviewed this recipe")

    # create rating and commit to db
    rating = model.Rating(
        rating=stars,
        recipe_id=recipe_id,
        user_id=current_user.id,
        comment=comment
    )
    
    db.session.add(rating)
    db.session.commit()


    # upload photo
    uploaded_photo = request.files['photo']
    if uploaded_photo.filename != '':
        content_type = uploaded_photo.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            flash("Invalid file type")
            abort(400, f"Unsupported file type {content_type}")
        
        new_photo = model.Photo(file_extension=file_extension, user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(new_photo)
        db.session.commit()

        path = (
            pathlib.Path(current_app.root_path)
            / "static"
            / "photos"
            / f"photo-{new_photo.id}.{file_extension}"
        )
        uploaded_photo.save(path)

    return redirect(url_for("recipe.recipe", recipe_id = recipe_id))




@bp.route("/edit_rating", methods=["POST"])
def edit_rating():

# CONTROLLER FOR EDITING RATINGS

# return redirect(url_for("recipe.recipe", recipe_id = recipe_id))
    return 0