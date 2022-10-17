from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import database

bp_app = Blueprint('application', __name__, url_prefix='/app')

@bp_app.route("/")
@bp_app.route("/<string:business>")
@bp_app.route("/<string:business>/<string:checker>")
@bp_app.route("/<string:business>/<string:checker>/<string:action>")
def application(business=None,checker=None,action=None):
    print(request.args)
    if not business or not checker or not action:
        return redirect(url_for('application.application',business=g.session, checker=g.user,action='sell'))
    else:
        return render_template("app/sell.html")