import random
from flask import Blueprint, request, redirect, url_for, flash
from .. import db, bcrypt
from . import model
import flask_login

import datetime

bp = Blueprint("auth", __name__)

@bp.route("/", methods=["POST"])
def login_signup(): # TODO: separate into two separate routes with views
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    if username:
        # Check that passwords are equal
        if password != request.form.get("password_repeat"):
            flash("Passwords were different")
            return redirect(url_for("main.index"))
        # Check if the email is already at the database
        query = db.select(model.User).where(model.User.email == email)
        user = db.session.execute(query).scalar_one_or_none()
        if user:
            flash("Email provided is already registered")
            return redirect(url_for("main.index"))
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
        flash("Invalid credentials")
        return redirect(url_for("main.index"))

@bp.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("main.index"))