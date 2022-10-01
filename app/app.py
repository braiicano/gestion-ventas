from flask import Flask, render_template, redirect, url_for, flash, request, g, session, escape
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)


def lock(hash: str):
    return generate_password_hash(hash, 'sha256')

DATA = ['USERNAME','EMAIL','FISCAL_NAME','BUNISESS_NAME','PHONE','ADDRESS','CUIT','IIBB','BEGIN_DATE','ITEM','IVA','CHECKERS']

class MYBUNISESS(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String(50), unique=True, nullable=False)
    EMAIL = db.Column(db.String(50), unique=True, nullable=False)
    PASSWORD = db.Column(db.String(100), nullable=False)
    PHONE = db.Column(db.String(30))
    ADDRESS = db.Column(db.String(255))
    FISCAL_NAME = db.Column(db.String(50))
    BUNISESS_NAME = db.Column(db.String(50))
    CUIT = db.Column(db.Integer)
    IIBB = db.Column(db.Integer)
    BEGIN_DATE = db.Column(db.String(255))
    ITEM = db.Column(db.Integer)
    IVA = db.Column(db.Integer)
    CHECKERS = db.Column(db.Integer)
    CREATE_AT = db.Column(db.DateTime, default=dt.today().ctime())
    TYPE_ACCOUNT = db.Column(db.Integer)


def add_business(args):
    return MYBUNISESS(USERNAME=args['username'], EMAIL=args['email'], PASSWORD=lock(args['password'],TYPE_ACCOUNT='Free'))


def check_db_users(data):
    print(data)
    user = MYBUNISESS.query.filter_by(USERNAME=data['username']).first()
    print(user)
    if not user:
        email = MYBUNISESS.query.filter_by(EMAIL=data['email']).first()
        print(email)
        if not email:
            return True
        else:
            return False
    else:
        return False


def verify_user(args):
    query = MYBUNISESS.query.filter_by(USERNAME=args['username']).first()
    if query and check_password_hash(query.PASSWORD, args['password']):
        session["new_user"] = query.USERNAME
        return True
    else:
        return False


def create_dict(args) -> dict:
    key = ['Nombre de usuario', 'Email', 'Nombre fiscal', 'Nombre comercial', 'Teléfono', 'Dirección',
           'CUIT', 'IIBB', 'Fecha de inicio', 'Rubro', 'IVA', 'Cajeros', 'Creación de cuenta', 'Tipo de cuenta']

    return {key[0]: args.USERNAME,
            key[1]:args.EMAIL,
            key[2]:args.FISCAL_NAME,
            key[3]:args.BUNISESS_NAME,
            key[4]:args.PHONE,
            key[5]:args.ADDRESS,
            key[6]:args.CUIT,
            key[7]:args.IIBB,
            key[8]:args.BEGIN_DATE,
            key[9]:args.ITEM,
            key[10]:args.IVA,
            key[11]:args.CHECKERS,
            key[12]:args.CREATE_AT,
            key[13]:args.TYPE_ACCOUNT,
            }

@ app.before_request
def before_request():
    if 'new_user' in session:
        g.user = session['new_user']
    else:
        g.user = None


@ app.route('/')
def index():
    if g.user:
        return redirect(url_for('application'))
    else:
        return redirect(url_for('signup'))


@ app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        if request.form['password'] == request.form['re-password']:
            if check_db_users(request.form):
                db.session.add(add_business(request.form))
                db.session.commit()
                session['new_user'] = request.form['username']
                flash("Te registraste correctamente", "success")
                return redirect(url_for('index'))
            else:
                flash("Usuario y/o email son existentes.", "warning")
        else:
            flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for('index'))


@ app.route('/login', methods=['POST'])
def login():
    if not g.user:
        if request.method == 'POST':
            if verify_user(request.form):
                flash(f"Hola {request.form['username']}", "success")
                return redirect(url_for('index'))
            flash("Usuario y/o contraseña no son correctos", "danger")
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('new_user', None)
    flash("Se ha cerrado sesión con éxito", "success")
    return redirect(url_for('index'))


@app.route('/app')
def application():
    if g.user:
        return render_template('app.html', login=True)
    flash("Debes iniciar sesión primero", "danger")
    return redirect(url_for("signup"))


@app.route('/app/admin')
def admin():
    if g.user:
        user = create_dict(MYBUNISESS.query.filter_by(USERNAME=g.user).first())
        return render_template('admin.html', login=True, user=user,data=DATA)
    flash("Debes iniciar sesión primero", "danger")
    return redirect(url_for("signup"))

@app.route('/update/admin', methods=['POST'])
def update_admin():
    print(request.form)
    return redirect(url_for('application'))

@app.errorhandler(404)
def error_handler(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8080)
