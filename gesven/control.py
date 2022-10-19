from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db import database, CHECKERS, REGISTER_OC, dt
from random import randrange

bp_control = Blueprint('control', __name__, url_prefix='/control')


@bp_control.route('/control', methods=['POST'])
def control():
    if request.args['option'] == 'open':
        o = REGISTER_OC(OPEN_DATE=dt.today().strftime("%Y-%m-%d"),
                        OPEN_TIME=dt.today().strftime("%H:%M:%S"),
                        OPEN_AMOUNT=request.form['open'],
                        CLOSE_DATE="",
                        CLOSE_TIME="",
                        CLOSE_AMOUNT=0,
                        TOTAL_AMOUNT=0)
        database.session.add(o)
        database.session.commit()
        g.status_check = session['status_check'] = 'OPEN'

    return redirect(url_for('application.application', business=g.session, checker=g.user, action='sell'))
