from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import database, PROVIDERS

bp_provider = Blueprint('provider', __name__, url_prefix='/provider')



@bp_provider.route('/providers', methods=['POST','GET'])
def provider():
    if request.method == 'POST':
        if request.args['option'] == 'new':
            r = request.form
            new_provider = PROVIDERS(NAME=r['NAME'], NAME_CONTACT=r['NAME_CONTACT'],
                                ADDR_STREET=r['ADDR_STREET'],
                                ADDR_CITY=r['ADDR_CITY'],
                                #  ADDR_COUNTRY=r['ADDR_COUNTRY'],
                                PHONE=r['PHONE'],
                                EMAIL=r['EMAIL'],
                                CUIT=r['CUIT'] if r['CUIT'] != "" else None,
                                BUSINESS_REF=g.session)
            database.session.add(new_provider)
            database.session.commit()
            flash(f"Proveedor cargado correctamente.", "success")
        
        if request.args['option'] == 'update':
            id = request.args['values']
            r = request.form
            c = PROVIDERS.query.filter_by(ID=id).first()
            c.NAME = r['NAME'] if r['NAME'] != c.NAME else c.NAME
            c.NAME_CONTACT = r['NAME_CONTACT'] if r['NAME_CONTACT'] != c.NAME_CONTACT else c.NAME_CONTACT
            c.CUIT = r['CUIT'] if r['CUIT'] != c.CUIT else c.CUIT
            c.ADDR_STREET = r['ADDR_STREET'] if r['ADDR_STREET'] != c.ADDR_STREET else c.ADDR_STREET
            c.ADDR_CITY = r['ADDR_CITY'] if r['ADDR_CITY'] != c.ADDR_CITY else c.ADDR_CITY
            c.PHONE = r['PHONE'] if r['PHONE'] != c.PHONE else c.PHONE
            c.EMAIL = r['EMAIL'] if r['EMAIL'] != c.EMAIL else c.EMAIL
            database.session.add(c)
            database.session.commit()
            flash('Datos actualizados correctamente.','success')

    else:
        try:
            if request.args['option'] == 'delete':
                r = request.args['values']
                c = PROVIDERS.query.filter_by(ID=r).first()
                database.session.delete(c)
                database.session.commit()
                message = f'Proveedor "{c.NAME}" eliminado con éxito'
                flash(message,'success')
        except:
            flash('No se encontraron datos a eliminar.','warning')

    return redirect(url_for('application.application', business=g.session, checker=g.user,action='providers'))