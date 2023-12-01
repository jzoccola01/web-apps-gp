import random
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db, bcrypt

from . import model
import flask_login

import pathlib
from flask import current_app

import datetime

bp = Blueprint("recipe_creation", __name__)

@bp.route("/create", methods=["POST"])
def create():
    title = request.form.get("recipe-name")
    description = request.form.get("recipe-desc")
    servings = float(request.form.get("servings"))
    cook_time = int(request.form.get("cook-time"))
    ingredient_count = int(request.form.get("ingredient-count"))
    ingredients = []
    quantities = []
    units = []
    for i in range(1, ingredient_count+1):
        ingredients.append(request.form.get("ingredient" + str(i)))
        quantities.append(float(request.form.get("quantity" + str(i))))
        units.append(request.form.get("unit" + str(i)))
    step_count = int(request.form.get("step-count"))
    steps = []
    for i in range(1, step_count+1):
        steps.append(request.form.get("step" + str(i)))

    user_id = flask_login.current_user.id
    
    new_recipe = model.Recipe(title=title, description=description, servings=servings, cook_time=cook_time, user_id=user_id)
    db.session.add(new_recipe)
    
    uploaded_photo = request.files['photo']
    if uploaded_photo.filename != '':
        content_type = uploaded_photo.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            flash("Invalid file type")
            return redirect(url_for("main.index"))
        
        new_photo = model.Photo(file_extension=file_extension, user_id=user_id, recipe=new_recipe)
        db.session.add(new_photo)
        db.session.commit()

        path = (
            pathlib.Path(current_app.root_path)
            / "static"
            / "photos"
            / f"photo-{new_photo.id}.{file_extension}"
        )
        uploaded_photo.save(path)
    

    for i in range(ingredient_count):
        query = db.select(model.Ingredient).where(model.Ingredient.name == ingredients[i])
        ingredient = db.session.execute(query).scalar_one_or_none()
        if not ingredient:
            ingredient = model.Ingredient(name=ingredients[i])
            db.session.add(ingredient)
        quantified_ingredient = model.QuantifiedIngredient(quantity=quantities[i], unit=units[i], ingredient=ingredient, recipe=new_recipe)
        db.session.add(quantified_ingredient)

    for i in range(step_count):
        step = model.Step(seq_number=i+1, description=steps[i], recipe=new_recipe)
        db.session.add(step)

    db.session.commit()

    return redirect(url_for("main.index")) #TODO: change to recipe view of new recipe