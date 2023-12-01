# import datetime
# import dateutil.tz

from flask import Blueprint, render_template
from . import model

bp = Blueprint("main", __name__)

# TODO: Make sure the user is logged in before they can access the profile page.

@bp.route("/")
def index():
    return render_template("main/index.html")