import random
from flask import Blueprint, request, redirect, url_for, flash, render_template
from .. import db, bcrypt
from . import model
import flask_login

import datetime

bp = Blueprint("auth", __name__)

@bp.route("/", methods=["POST"])
def login_signup():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    query = db.select(model.Recipe).join(model.Rating, isouter=True).group_by(model.Recipe.id).order_by(db.func.avg(model.Rating.rating).desc())
    recipes = db.session.execute(query).scalars().all()

    bookmarks = []
    if flask_login.current_user.is_authenticated:
        query = db.select(model.Bookmark).where(model.Bookmark.user_id == flask_login.current_user.id)
        bookmarks = db.session.execute(query).scalars().all()

    if username:
        # Check that passwords are equal
        if password != request.form.get("password_repeat"):
            flash("Passwords did not match", 'auth')
            return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort="option1", category="All", search="", login=False, signup=True)
        # Check if the email is already at the database
        query = db.select(model.User).where(model.User.email == email)
        user = db.session.execute(query).scalar_one_or_none()
        if user:
            flash("Email is already registered", 'auth')
            return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort="option1", category="All", search="", login=False, signup=True)
        salt = random.randint(0, 100000)
        password_hash = bcrypt.generate_password_hash(password + str(salt)).decode("utf-8")
        new_user = model.User(email=email, username=username, password=password_hash, salt=salt, timestamp=datetime.datetime.now())
        db.session.add(new_user)
        db.session.commit()
        flask_login.login_user(new_user)
        # flash("Successfully signed up!")
        return redirect(url_for("main.index"))
    else:
        email = request.form.get("email")
    password = request.form.get("password")
    query = db.select(model.User).where(model.User.email == email)
    user = db.session.execute(query).scalar_one_or_none()
    if user and bcrypt.check_password_hash(user.password, password + str(user.salt)):
        flask_login.login_user(user)
        return redirect(url_for("main.index"))
    else:
        flash("Invalid credentials", 'auth')
        return render_template("main/index.html", recipes=recipes, bookmarks=bookmarks, sort="option1", category="All", search="", login=True, signup=False)

@bp.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("main.index"))