from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from db import ARTICLES, CHECKERS, PROVIDERS, CLIENTS, MYBUSINESS
from checker import pin_generator

bp_app = Blueprint('application', __name__, url_prefix='/app')


@bp_app.route("/")
@bp_app.route("/<string:business>")
@bp_app.route("/<string:business>/<string:checker>")
@bp_app.route("/<string:business>/<string:checker>/<string:action>")
def application(business=None, checker=None, action=None):
    print(action)
    if not business or not checker or not action:
        return redirect(url_for('application.application', business=g.session, checker=g.user, action='sell'))
    else:
        if action == 'sell':
            return render_template("app/sells.html")
        if action == 'check':
            return render_template("app/checkers.html")
        if action == 'articles':
            g.list_articles = ARTICLES.query.filter_by(
                BUSINESS_REF=g.session).all()
            g.list_providers = PROVIDERS.query.filter_by(
                BUSINESS_REF=g.session).all()
            return render_template("app/articles.html")
        if action == 'clients':
            g.list_clients = CLIENTS.query.filter_by(
                BUSINESS_REF=g.session).all()
            return render_template("app/clients.html")
        if action == 'providers':
            g.list_providers = PROVIDERS.query.filter_by(
                BUSINESS_REF=g.session).all()
            return render_template("app/providers.html")
        if action == 'modify':
            g.modify = CHECKERS.query.filter_by(ID=g.check_id).first()
            return render_template("app/modify.html")
        if action == 'admin':
            if g.type_user == 'admin':
                g.PIN = pin_generator()
                g.admin = MYBUSINESS.query.filter_by(
                    USERNAME=g.session).first()
                g.list_checkers = CHECKERS.query.filter_by(
                    BUSINESS_REF=g.session).all()
                return render_template("app/admin.html")
            else:
                flash('No tenés permisos suficientes para esta sección', 'danger')

        return redirect(url_for('application.application', business=g.session, checker=g.user, action='sell'))


@bp_app.route('/upload_csv', methods=['POST'])
def upload_csv():
    pass
