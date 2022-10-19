from flask import Flask, g, session
from auth import *
from checker import *
from application import *
from client import *
from provider import *
from article import *
from control import *

import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'developer'
app.register_blueprint(bp_auth)
app.register_blueprint(bp_checker)
app.register_blueprint(bp_client)
app.register_blueprint(bp_provider)
app.register_blueprint(bp_article)
app.register_blueprint(bp_control)
app.register_blueprint(bp_app)


@app.before_request
def before_request():
    print(session)
    if 'new_session' in session:
        g.session = session['new_session']
        if 'checker' in session:
            g.user = session['checker']
        else:
            g.user = None
        if 'type' in session:
            g.type_user = session['type']
        if 'id_checker' in session:
            g.check_id = session['id_checker']
        else:
            g.check_id = None
        if 'status_check' in session:
            g.status_check = session['status_check']

    else:
        g.session = None
        g.user = None
        g.type_user = None
        g.check_id = None
        g.status_check = None

@app.route('/')
def index():
    if g.session:
        return redirect(url_for('checker.auth'))
    else:
        return redirect(url_for('auth.auth'))

@app.errorhandler(404)
def error_404(e):
    return render_template('error.html',error=True),404

if __name__ == '__main__':
    db.database.init_app(app)
    app.run(debug=1, port=5000)
