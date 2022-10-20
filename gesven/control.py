from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from db import database, CHECKERS, REGISTER_OC, dt
from random import randrange

bp_control = Blueprint('control', __name__, url_prefix='/control')

# Modificar de 0 la gestion de apertura y cierre de caja, agregar un status a caja abierta o cerrada en mi cajero


@bp_control.route('/control', methods=['POST'])
def control():
    if request.args['option'] == 'open':
        o = REGISTER_OC(OPEN_DATE=dt.today().strftime("%Y-%m-%d"),
                        OPEN_TIME=dt.today().strftime("%H:%M:%S"),
                        OPEN_AMOUNT=float(request.form['open']),
                        CHECKER_ID=g.check_id,
                        BUSINESS_REF=g.session)
        c = CHECKERS.query.filter_by(ID=g.check_id).first()
        c.STATUS_CHECK = f"OPEN|{o.OPEN_DATE}|{o.OPEN_TIME}|{o.OPEN_AMOUNT}"
        database.session.add_all([o, c])
        database.session.commit()
        g.status_check = session['status_check'] = c.STATUS_CHECK
    if request.args['option'] == 'close':
        c = CHECKERS.query.filter_by(ID=g.check_id).first()
        STATUS: str = c.STATUS_CHECK.split('|')
        o = REGISTER_OC.query.filter_by(CHECKER_ID=g.check_id).filter_by(
            OPEN_DATE=STATUS[1]).filter_by(OPEN_TIME=STATUS[2]).first()
        o.CLOSE_DATE = dt.today().strftime("%Y-%m-%d")
        o.CLOSE_TIME = dt.today().strftime("%H:%M:%S")
        o.CLOSE_AMOUNT = float(request.form['close'])
        o.TOTAL_AMOUNT = o.CLOSE_AMOUNT - o.OPEN_AMOUNT
        c.STATUS_CHECK = f"CLOSE"
        database.session.add_all([o, c])
        database.session.commit()
        g.status_check = session['status_check'] = 'CLOSE'

    return redirect(url_for('application.application', business=g.session, checker=g.user, action='sell'))
