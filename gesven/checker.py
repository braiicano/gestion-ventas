from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import MYBUSINESS, database, CHECKERS
from random import randrange

bp_checker = Blueprint('checker', __name__, url_prefix='/checker')


def pin_generator() -> int:
    return randrange(1000, 9999)


@bp_checker.route('/add_checker', methods=['POST'])
def add_checker():
    verify = None
    TYPE_USER = 0
    if request.args['option'] == 'admin':
        if request.form['NAME'] and len(request.form['PIN']) > 3:
            if request.form['PIN'] == request.form['CONFIRM-PIN']:
                verify = True
                TYPE_USER = 2
            else:
                flash("El PIN ingresado no coincide", "danger")
        elif not request.form['NAME']:
            flash('Es necesario que ingreses tu nombre.', 'danger')
        elif len(request.form['PIN']) <= 3:
            flash('El PIN debe contener al menos 4 números.', 'warning')
    if request.args['option'] == 'new':
        if not '' == [request.form['NAME'], request.form['SURNAME']]:
            verify = True
            TYPE_USER = 1

    if verify:
        r = request.form
        new_check = CHECKERS(NAME=r['NAME'], SURNAME=r['SURNAME'],
                             BIRTH_DAY=r['BIRTH_DAY'] if r['BIRTH_DAY'] != "" else None,
                             ADDR_STREET=r['ADDR_STREET'],
                             ADDR_CITY=r['ADDR_CITY'],
                             ADDR_COUNTRY=r['ADDR_COUNTRY'],
                             PHONE=r['PHONE'],
                             EMAIL=r['EMAIL'],
                             DU=r['DU'] if r['DU'] != "" else None,
                             PIN=r['PIN'],
                             TYPE_USER=TYPE_USER,
                             BUSINESS_REF=g.session)
        database.session.add(new_check)
        database.session.commit()
        if TYPE_USER == 2:
            g.type_user = session['type'] = 'checker' if TYPE_USER == 1 else 'admin'
            g.user = session['checker'] = f"{r['NAME']}{r['SURNAME']}"
            session['id_checker'] = CHECKERS.query.filter_by(BUSINESS_REF=g.session).filter_by(NAME=r['NAME']).first().ID
            g.check_id = session['id_checker']
            flash(f"Bienvenido {g.user}", "success")
        if TYPE_USER == 1:
            flash(f'Se dió de alta al cajero "{r["NAME"]}"', 'success')
        return redirect(url_for('application.application', business=g.session, checker=g.user))
    else:
        return redirect(url_for('checker.auth'))


@bp_checker.route('/users', methods=['POST','GET'])
def users():
    if request.args['option'] == 'login':
        r = request.form
        if r['USER']:
            c = CHECKERS.query.filter_by(BUSINESS_REF=g.session).filter_by(NAME=r['USER'].split('$$')[0]).filter_by(
                SURNAME=r['USER'].split('$$')[1]).first()
            if c.PIN == int(r['PIN']):
                session['type'] = 'checker' if c.TYPE_USER == 1 else 'admin'
                g.type_user = session['type']
                g.check_id = session['id_checker'] = c.ID
                g.user = session['checker'] = r['USER'].replace('$', '')
            else:
                flash("Pin ingresado no es válido", "danger")
        else:
            flash('No se detectó selección, debe elegir un usuario.', 'warning')
    if request.args['option'] == 'update':
        if request.form['NAME'] and request.form['SURNAME'] and request.form['DU']:
            id = request.args['values']
            r = request.form
            BIRTH_DAY = None if r['BIRTH_DAY'] == '' else r['BIRTH_DAY']
            c = CHECKERS.query.filter_by(ID=id).first()
            c.NAME = r['NAME'] if r['NAME'] != c.NAME else c.NAME
            c.SURNAME = r['SURNAME'] if r['SURNAME'] != c.SURNAME else c.SURNAME
            c.DU = r['DU'] if r['DU'] != c.DU else c.DU
            c.BIRTH_DAY = BIRTH_DAY if BIRTH_DAY != c.BIRTH_DAY else c.BIRTH_DAY
            c.ADDR_STREET = r['ADDR_STREET'] if r['ADDR_STREET'] != c.ADDR_STREET else c.ADDR_STREET
            c.ADDR_CITY = r['ADDR_CITY'] if r['ADDR_CITY'] != c.ADDR_CITY else c.ADDR_CITY
            c.PHONE = r['PHONE'] if r['PHONE'] != c.PHONE else c.PHONE
            c.EMAIL = r['EMAIL'] if r['EMAIL'] != c.EMAIL else c.EMAIL
            c.PIN = r['PIN'] if r['PIN'] != c.PIN else c.PIN
            database.session.add(c)
            database.session.commit()
            flash('Datos actualizados correctamente.', 'success')
        else:
            r = request.form
            message = []
            if r['NAME'] == '':
                message.append('Nombre')
            if r['SURNAME'] == '':
                message.append('Apellido')
            if r['DU'] == '':
                message.append('Documento')
            message = message.__str__().strip('\[\]')
            flash(
                f'Los siguientes campos no pueden estar vacíos: {message}', 'warning')
    if request.args['option'] == 'admin':
        r = request.form
        BEGIN_TIME = None if r['BEGIN_TIME'] == '' else r['BEGIN_TIME']
        CUIT = None if r['CUIT'] == '' else r['CUIT']
        IIBB = None if r['IIBB'] == '' else r['IIBB']
        IVA = None if r['IVA'] == '' else r['IVA']
        c = MYBUSINESS.query.filter_by(USERNAME=g.session).first()
        c.PHONE = r['PHONE'] if r['PHONE'] != c.PHONE else c.PHONE
        c.BEGIN_TIME = BEGIN_TIME if BEGIN_TIME != c.BEGIN_TIME else c.BEGIN_TIME
        c.ADDR_STREET = r['ADDR_STREET'] if r['ADDR_STREET'] != c.ADDR_STREET else c.ADDR_STREET
        c.ADDR_CITY = r['ADDR_CITY'] if r['ADDR_CITY'] != c.ADDR_CITY else c.ADDR_CITY
        c.ADDR_COUNTRY = r['ADDR_COUNTRY'] if r['ADDR_COUNTRY'] != c.ADDR_COUNTRY else c.ADDR_COUNTRY
        c.FISCAL_NAME = r['FISCAL_NAME'] if r['FISCAL_NAME'] != c.FISCAL_NAME else c.FISCAL_NAME
        c.BUSINESS_NAME = r['BUSINESS_NAME'] if r['BUSINESS_NAME'] != c.BUSINESS_NAME else c.BUSINESS_NAME
        c.CUIT = CUIT if CUIT != c.CUIT else c.CUIT
        c.IVA = IVA if IVA != c.IVA else c.IVA
        c.IIBB = IIBB if IIBB != c.IIBB else c.IIBB
        c.ITEM = r['ITEM'] if r['ITEM'] != c.ITEM else c.ITEM
        database.session.add(c)
        database.session.commit()
        flash('Datos actualizados correctamente.', 'success')
    if request.args['option'] == 'delete':
        try:
            if request.args['option'] == 'delete':
                r = request.args['values']
                c = CHECKERS.query.filter_by(ID=r).first()
                database.session.delete(c)
                database.session.commit()
                message = f'Cliente "{c.NAME}" eliminado con éxito'
                flash(message,'success')
        except:
            flash('No se encontraron datos a eliminar.','warning')
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
    session.pop('type', None)
    session.pop('id_checker', None)
    session.pop('status_check', None)
    return redirect(url_for('checker.auth'))
