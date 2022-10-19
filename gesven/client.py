from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)
from db import database, dt, CLIENTS

bp_client = Blueprint('client', __name__, url_prefix='/client')


@bp_client.route('/', methods=['POST','GET'])
def client():
    modify = None
    if request.method == 'POST':
        r = request.form
        if not '' in [r['DOCUMENT'], r['NAME'], r['SURNAME']]:
            if request.args['option'] == 'new':
                c = CLIENTS(NAME=r['NAME'], SURNAME=r['SURNAME'], BIRTH_DAY=None if r['BIRTH_DAY'] == '' else r['BIRTH_DAY'],
                            ADDR_STREET=r['ADDR_STREET'], ADDR_CITY=r['ADDR_CITY'], PHONE=r['PHONE'], EMAIL=r['EMAIL'],
                            DU=r['DOCUMENT'], BUSINESS_REF=g.session)
                modify = 'NEW_CLIENT'
            if request.args['option'] == 'update':
                BIRTH_DAY = None if r['BIRTH_DAY'] == '' else r['BIRTH_DAY']
                c = CLIENTS.query.filter_by(ID=request.args['values']).first()
                c.NAME = r['NAME'] if c.NAME != r['NAME'] else c.NAME
                c.SURNAME = r['SURNAME'] if c.SURNAME != r['SURNAME'] else c.SURNAME
                c.BIRTH_DAY = BIRTH_DAY if c.BIRTH_DAY != BIRTH_DAY else c.BIRTH_DAY
                c.ADDR_STREET = r['ADDR_STREET'] if c.ADDR_STREET != r['ADDR_STREET'] else c.ADDR_STREET
                c.ADDR_CITY = r['ADDR_CITY'] if c.ADDR_CITY != r['ADDR_CITY'] else c.ADDR_CITY
                c.PHONE = r['PHONE'] if c.PHONE != r['PHONE'] else c.PHONE
                c.EMAIL = r['EMAIL'] if c.EMAIL != r['EMAIL'] else c.EMAIL
                c.DU = r['DOCUMENT'] if c.DU != r['DOCUMENT'] else c.DU
                c.LAST_UPDATE = dt.today().strftime("%Y-%m-%d %H:%M:%S")
                modify = 'UPDATE_CLIENT'
            if modify:
                try:
                    database.session.add(c)
                    database.session.commit()
                    message = 'Nuevo cliente agregado' if modify == 'NEW_CLIENT' else 'Datos actualizados correctamente'
                    flash(message, 'success')
                except:
                    if modify == 'NEW_CLIENT':
                        flash(f'Cliente "{r["NAME"]}" ya existe.','warning')
                    if modify == 'UPDATE_CLIENT':
                        flash(f'Error al intentar actualizar datos.','danger')
        else:
            message = []
            if r['NAME'] == '':
                message.append('Nombre')
            if r['SURNAME'] == '':
                message.append('Apellido')
            if r['DOCUMENT'] == '':
                message.append('Documento')
            message = message.__str__().strip('\[\]')
            flash(f"Los campos no pueden estar vacios. {message}", "warning")
    else:
        try:
            if request.args['option'] == 'delete':
                r = request.args['values']
                c = CLIENTS.query.filter_by(ID=r).first()
                database.session.delete(c)
                database.session.commit()
                message = f'Cliente "{c.NAME}" eliminado con éxito'
                flash(message,'success')
        except:
            flash('No se encontraron datos a eliminar.','warning')
    return redirect(url_for('application.application', business=g.session, checker=g.user, action='clients'))
