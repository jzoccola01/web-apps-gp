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


### GET RECIPE PAGE ###
@bp.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):

    recipe = db.get_or_404(model.Recipe, recipe_id)

    # Query for average of reviews out of 5 stars for specific recipe
    rating_value = db.session.query(func.avg(model.Rating.rating)).where(model.Rating.recipe_id == recipe.id).scalar()
    if (type(rating_value) == float):
        rating_value = round(rating_value, 1)
    else:
        rating_value = "Not Yet Rated"


    # check if user has already submitted a review
    if current_user.is_authenticated:
        query = db.select(model.Rating).where(model.Rating.user_id == current_user.id).where(model.Rating.recipe_id == recipe_id)
        previous = db.session.execute(query).scalars().all()
        if(len(previous) == 0):
            previously_rated = 0
            previous_rating=0
        else:
            previously_rated = 1
            previous_rating=previous[0]
    else:
        previously_rated = 0
        previous_rating=0


    # query bookmarks
    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()

    return render_template("main/recipe.html", recipe=recipe, rating_value=rating_value, previously_rated=previously_rated, previous_rating=previous_rating, bookmarks=bookmarks)



### CREATE NEW RATING ###
@bp.route("/new_rating", methods=["POST"])
def new_rating():
    comment = request.form.get("text")
    stars = request.form.get("stars")
    recipe_id = request.form.get("recipe_id")

    if(stars == None):
        stars = 1

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



### EDIT CURRENT USER'S RATING ###
@bp.route("/edit_rating", methods=["POST"])
def edit_rating():
    previous_rating_id = request.form.get("previous_rating_id")
    query = db.select(model.Rating).where(model.Rating.id == previous_rating_id)
    current_rating = db.session.execute(query).scalar_one()


    comment = request.form.get("text")
    rating = request.form.get("stars")
    recipe_id = request.form.get("recipe_id")

    if(rating == None):
        rating = 1

    current_rating.rating = rating
    current_rating.comment = comment

    db.session.commit()

    return redirect(url_for("recipe.recipe", recipe_id = recipe_id))


### DELETE CURRENT USER'S RATING ###
@bp.route("/delete_rating", methods=["POST"])
def delete_rating():
    previous_rating_id = request.form.get("previous_rating_id")
    query = db.select(model.Rating).where(model.Rating.id == previous_rating_id)
    current_rating = db.session.execute(query).scalar_one()

    db.session.delete(current_rating)
    db.session.commit()

    recipe_id = request.form.get("recipe_id")

    return redirect(url_for("recipe.recipe", recipe_id = recipe_id))




### BOOKMARK RECIPE ###
@bp.route("/recipe_bookmark", methods=["POST"])
@flask_login.login_required
def recipe_bookmark():
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

    return redirect(url_for("recipe.recipe", recipe_id = recipe_id))