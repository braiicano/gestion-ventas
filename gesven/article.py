from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from db import database, dt, ARTICLES

bp_article = Blueprint('article', __name__, url_prefix='/article')


@bp_article.route('/', methods=['POST', 'GET'])
def article():
    modify = None
    if request.method == 'POST':
        r = request.form
        if not '' in [r['NAME'], r['COST']]:
            COST = float(r['COST']) if r['COST'] != '' else 0
            PUBLIC_PRICE = float(
                r['PUBLIC_PRICE']) if r['PUBLIC_PRICE'] != '' else 0
            STOCK = int(r['STOCK']) if r['STOCK'] != '' else 0
            IVA = int(r['IVA']) if r['IVA'] != '' else 0
    
            try:
                ACTIVE = "on" if r['ACTIVE'] else "off"
            except:
                ACTIVE = "off"
            if request.args['option'] == 'new':
                c = ARTICLES(NAME=r['NAME'], CATEGORY=r['CATEGORY'], PROVIDER=r['PROVIDER'],
                             MAKER=r['MAKER'], SKU=r['SKU'], STOCK=STOCK,
                             COST=COST,
                             PUBLIC_PRICE=PUBLIC_PRICE,
                             PROFIT=PUBLIC_PRICE-COST, IVA=IVA, ACTIVE=ACTIVE, BUSINESS_REF=g.session)
                modify = 'NEW_ARTICLE'
            if request.args['option'] == 'update':
                c = ARTICLES.query.filter_by(ID=request.args['values']).first()
                c.NAME = r['NAME'] if c.NAME != r['NAME'] else c.NAME
                c.CATEGORY = r['CATEGORY'] if c.CATEGORY != r['CATEGORY'] else c.CATEGORY
                c.PROVIDER = r['PROVIDER'] if c.PROVIDER != r['PROVIDER'] else c.PROVIDER
                c.MAKER = r['MAKER'] if c.MAKER != r['MAKER'] else c.MAKER
                c.SKU = r['SKU'] if c.SKU != r['SKU'] else c.SKU
                c.STOCK = STOCK if c.STOCK != STOCK else c.STOCK
                c.COST = COST if c.COST != COST else c.COST
                c.PUBLIC_PRICE = PUBLIC_PRICE if c.PUBLIC_PRICE != PUBLIC_PRICE else c.PUBLIC_PRICE
                c.IVA = IVA if c.IVA != IVA else c.IVA
                c.ACTIVE = r['ACTIVE'] if c.ACTIVE != r['ACTIVE'] else c.ACTIVE
                c.PROFIT = (PUBLIC_PRICE-COST)
                c.LAST_UPDATE = dt.today().strftime("%Y-%m-%d %H:%M:%S")
                modify = 'UPDATE_ARTICLE'
            if modify:
                # try:
                    database.session.add(c)
                    database.session.commit()
                    message = 'Nuevo artículo agregado' if modify == 'NEW_ARTICLE' else 'Datos actualizados correctamente'
                    flash(message, 'success')
                # except:
                #     if modify == 'NEW_ARTICLE':
                #         flash(f'Artículo "{r["NAME"]}" ya existe.', 'warning')
                #     if modify == 'UPDATE_ARTICLE':
                #         flash(f'Error al intentar actualizar datos.', 'danger')
        else:
            message = []
            if r['NAME'] == '':
                message.append('Nombre')
            if r['COST'] == '':
                message.append('Costo')
            message = message.__str__().strip('\[\]')
            flash(f"Los campos no pueden estar vacios. {message}", "warning")
    else:
        try:
            if request.args['option'] == 'delete':
                r = request.args['values']
                c = ARTICLES.query.filter_by(ID=r).first()
                database.session.delete(c)
                database.session.commit()
                message = f'Artículo "{c.NAME}" eliminado con éxito'
                flash(message, 'success')
        except:
            flash('No se encontraron datos a eliminar.', 'warning')
    return redirect(url_for('application.application', business=g.session, checker=g.user, action='articles'))
