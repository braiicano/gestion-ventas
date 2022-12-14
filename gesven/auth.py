from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import database, MYBUSINESS
from werkzeug.security import generate_password_hash, check_password_hash
from control import verifySecurity

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
        q = verifySecurity(request.form['PASSWORD'])
        if q == True:
            db = MYBUSINESS.query.filter_by(
                USERNAME=values['USERNAME']).first()
            if option == 'login':
                if None != db:
                    if check_password_hash(db.PASSWORD, values['PASSWORD']):
                        g.session = session['new_session'] = values['USERNAME']
                        session['id_business'] = db.ID
                        return True
                    else:
                        flash('Error al validar credenciales.', 'warning')
                else:
                    flash('Usuario no encontrado', 'danger')
            elif option == 'signup':
                if None == db:
                    email = MYBUSINESS.query.filter_by(
                        EMAIL=values['EMAIL']).first()
                    if None == email:
                        if values['PASSWORD'] == values['CONFIRM-PASSWORD']:

                            new_user = MYBUSINESS(USERNAME=values['USERNAME'], PASSWORD=lock(
                                values['PASSWORD']), EMAIL=values['EMAIL'])
                            database.session.add(new_user)
                            database.session.commit()
                            g.session = session['new_session'] = values['USERNAME']
                            session['id_business'] = MYBUSINESS.query.filter_by(
                                USERNAME=g.session).first().ID
                            return redirect(url_for('checker.auth'))
                        else:
                            flash('Las contraseñas no coinciden.', 'warning')
                    else:
                        flash('Ya existe el email ingresado', 'info')
                else:
                    flash('Ya existe el usuario "%s"' %
                          values['USERNAME'], 'info')
        else:
            flash(f"Contraseña débil: {q}", "danger")


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
    session.pop('checker', None)
    session.pop('id_business', None)
    session.pop('id_checker', None)
    session.pop('new_session', None)
    session.pop('status_check', None)
    session.pop('type', None)
    flash('Cerraste sesion con éxito', 'info')
    return redirect(url_for('auth.auth'))
