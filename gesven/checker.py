from crypt import methods
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import database, CHECKERS
from random import randrange

bp_checker = Blueprint('checker', __name__, url_prefix='/checker')


def pin_generator() -> int:
    return randrange(1000, 9999)


@bp_checker.route('/add_checker', methods=['POST'])
def add_checker():
    verify = None
    if request.args['option'] == 'admin':
        if request.form['name'] and len(request.form['pin']) > 3:
            if request.form['pin'] == request.form['confirm-pin']:
                verify = True
            else:
                flash("El pin ingresado no coincide", "danger")
        elif not request.form['name']:
            flash('Es necesario que ingreses tu nombre.', 'danger')
        elif len(request.form['pin']) <= 3:
            flash('El pin debe contener al menos 4 números.', 'warning')
    if verify:
        r = request.form
        new_check = CHECKERS(NAME=r['name'], SURNAME=r['surname'],
                             BIRTH_DAY=r['birth_day'] if r['birth_day'] != "" else None,
                             ADDR_STREET=r['addr_street'],
                             ADDR_CITY=r['addr_city'],
                             ADDR_COUNTRY=r['addr_country'],
                             PHONE=r['phone'],
                             EMAIL=r['email'],
                             DU=r['du'] if r['du'] != "" else None,
                             PIN=r['pin'],
                             TYPE_USER=2,
                             BUSINESS_REF=g.session)
        database.session.add(new_check)
        database.session.commit()
        g.user = session['checker'] = r['name']
        flash(f"Bienvenido {g.user}", "success")
        return redirect(url_for('application.application', business=g.session, checker=g.user))
    else:
        return redirect(url_for('checker.auth'))


@bp_checker.route('/users', methods=['POST'])
def users():
    if request.args['option'] == 'login':
        r = request.form
        print(r['user'].replace('$',''))
        if r['user']:
            c = CHECKERS.query.filter_by(NAME=r['user'].split('$$')[0]).filter_by(SURNAME=r['user'].split('$$')[1]).first()
            if c.PIN == int(r['pin']):
                g.check = session['checker'] = r['user'].replace('$','')
            else:
                flash("Pin ingresado no es válido","danger")
        else:
            flash('No se detectó selección, debe elegir un usuario.','warning')
    return redirect(url_for('checker.auth'))


@bp_checker.route('/')
def auth():
    if g.user:
        return redirect(url_for('application.application'))
    else:
        # try:
        check = CHECKERS.query.filter_by(BUSINESS_REF=g.session).first()
        if check:
            g.check_session = True
            g.list_checkers = CHECKERS.query.filter_by(
                BUSINESS_REF=g.session).all()
        else:
            g.check_session = None
            g.PIN = pin_generator()
        return render_template('checkers/auth.html')


@bp_checker.route('/logout')
def logout():
    session.pop('checker', None)
    return redirect(url_for('checker.auth'))
