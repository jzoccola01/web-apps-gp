import datetime
import dateutil.tz
from sqlalchemy import func
from flask import Blueprint, render_template, request, url_for, redirect

from . import model
from . import db

bp = Blueprint("profile", __name__)



@bp.route("/profile")
def profile():
    return render_template("main/profile.html")