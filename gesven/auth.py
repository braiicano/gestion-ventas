from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import database, MYBUSINESS
from werkzeug.security import generate_password_hash, check_password_hash

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


def lock(password):
    return generate_password_hash(password, 'sha256')


def verify_form(values: dict, option: str = ''):
    verify = False
    for k, v in values.items():
        if v == '':
            flash(f'El campo "{k}" no puede estar vacío', 'danger')
            return False
        else:
            verify = True
    if verify:
        db = MYBUSINESS.query.filter_by(USERNAME=values['username']).first()
        if option == 'login':
            if None != db:
                if check_password_hash(db.PASSWORD, values['password']):
                    g.session = session['new_session'] = values['username']
                    session['id_business'] = db.ID
                    return True
                else:
                    flash('Error al validar credenciales.', 'warning')
            else:
                flash('Usuario no encontrado', 'danger')
        elif option == 'signup':
            if None == db:
                email = MYBUSINESS.query.filter_by(
                    EMAIL=values['email']).first()
                if None == email:
                    if values['password'] == values['confirm-password']:
                        new_user = MYBUSINESS(USERNAME=values['username'], PASSWORD=lock(
                            values['password']), EMAIL=values['email'])
                        database.session.add(new_user)
                        database.session.commit()
                        g.session = session['new_session'] = values['username']
                        session['id_business'] = MYBUSINESS.query.filter_by(
                            USERNAME=g.session).first().ID
                        return redirect(url_for('checker.auth'))
                    else:
                        flash('Las contraseñas no coinciden.', 'warning')
                else:
                    flash('Ya existe el email ingresado', 'info')
            else:
                flash('Ya existe el usuario "%s"' % values['username'], 'info')


@bp_auth.route('/', methods=['GET', 'POST'])
def auth():
    if g.session:
        return redirect(url_for('checker.auth'))
    else:
        if request.method == 'POST':
            if verify_form(request.form, request.args['option']):
                return redirect(url_for('checker.auth'))
            return render_template('auth/auth.html')
        else:
            return render_template('auth/auth.html')


@bp_auth.route('/logout')
def logout():
    session.pop('new_session', None)
    session.pop('checker',None)
    session.pop('id_business',None)
    flash('Cerraste sesion con éxito', 'info')
    return redirect(url_for('auth.auth'))
