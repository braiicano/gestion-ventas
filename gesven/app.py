from email.mime import application
from flask import Flask, g, session
from auth import *
from checker import *
from application import *

import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'developer'
app.register_blueprint(bp_auth)
app.register_blueprint(bp_checker)
app.register_blueprint(bp_app)


@app.before_request
def before_request():
    print(session,g)
    if 'new_session' in session:
        g.session = session['new_session']
        if 'checker' in session:
            g.user = session['checker']
        else:
            g.user = None
    else:
        g.session = None
        g.user = None


if __name__ == '__main__':
    db.database.init_app(app)
    app.run(debug=1, port=5000)
