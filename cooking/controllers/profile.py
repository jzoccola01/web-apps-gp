from flask import Blueprint, render_template, abort
from . import model
from .. import db

bp = Blueprint("profile", __name__)

@bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = db.session.get(model.User, user_id)
    if not user:
        abort(404, "User with id {} doesn't exist.".format(user_id))
    return render_template('main/profile.html', user=user)