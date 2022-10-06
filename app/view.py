from flask import Flask, render_template, redirect, url_for, flash, request, g, session, escape
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
import sqlalchemy.exc as error
from werkzeug.security import generate_password_hash, check_password_hash
from random import randrange, randint
import os


dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)


def ra() -> int:
    return randrange(1000, 9999)


def lock(hash: str):
    return generate_password_hash(hash, 'sha256')


DATA = ['USERNAME', 'EMAIL', 'FISCAL_NAME', 'BUSINESS_NAME', 'PHONE',
        'ADDRESS', 'CUIT', 'IIBB', 'BEGIN_DATE', 'ITEM', 'IVA', 'CHECKERS']
CHECK_DATA = ['NAME', 'SURNAME', 'BIRTH_DAY',
              'ADDRESS', 'PHONE', 'EMAIL', 'TYPE_USER', 'PIN']


class BASE(db.Model):
    __abstract__ = True
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50), nullable=False)
    SURNAME = db.Column(db.String(50), nullable=False)
    BIRTH_DAY = db.Column(db.String(255))
    ADDRESS = db.Column(db.String(50))
    PHONE = db.Column(db.String(50))
    EMAIL = db.Column(db.String(50))
    LAST_UPDATE = db.Column(db.DateTime, default=dt.today())


class ARTICLES(db.Model):
    __tablename__ = 'ARTICLES'
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50), nullable=False)
    CATEGORY = db.Column(db.String(50))
    PROVIDER = db.Column(db.String(50))
    SKU = db.Column(db.String(50))
    STOCK = db.Column(db.Integer)
    COST = db.Column(db.Integer, default=0)
    IVA = db.Column(db.Integer, default=0)
    SALE = db.Column(db.Integer, default=1)  # where 0=no active, 1=active
    LAST_UPDATE = db.Column(db.DateTime, default=dt.today())
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))
    #IMAGE = db.Column(db.BLOB)


class INVOICE(db.Model):
    __tablename__ = 'INVOICE'
    ID = db.Column(db.Integer, primary_key=True)
    TYPE_INVOICE = db.Column(db.String, nullable=False)
    DATE = db.Column(db.DateTime, default=dt.today())
    ID_ARTICLE = db.Column(db.String(50))


class TYPE_ACCOUNT(db.Model):
    __tablename__ = 'TYPE_ACCOUNT'
    ID_Rel = db.relationship('MYBUSINESS', backref='onwer', lazy='dynamic')
    ID = db.Column(db.Integer, primary_key=True)
    TYPE = db.Column(db.String(10))


class MYBUSINESS(db.Model):
    __tablename__ = 'MYBUSINESS'
    ID = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String(50), unique=True, nullable=False)
    EMAIL = db.Column(db.String(50), unique=True, nullable=False)
    PASSWORD = db.Column(db.String(100), nullable=False)
    PHONE = db.Column(db.String(30))
    ADDRESS = db.Column(db.String(255))
    FISCAL_NAME = db.Column(db.String(50))
    BUSINESS_NAME = db.Column(db.String(50))
    CUIT = db.Column(db.Integer)
    IIBB = db.Column(db.Integer)
    BEGIN_DATE = db.Column(db.String(255))
    ITEM = db.Column(db.Integer)
    IVA = db.Column(db.Integer)
    CHECKERS = db.Column(db.Integer)
    CREATE_AT = db.Column(db.DateTime, default=dt.today())
    TYPE_ACCOUNT = db.Column(db.Integer, db.ForeignKey(
        'TYPE_ACCOUNT.ID'))


class CLIENTS(BASE):
    __tablename__ = 'CLIENTS'
    INVOICE = db.Column(db.Integer, db.ForeignKey('INVOICE.ID'))


class CHECKERS(BASE):
    __tablename__ = 'CHECKERS'
    TYPE_USER = db.Column(db.Integer, nullable=False)  # If 1=admin,2=check
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))
    PIN = db.Column(db.Integer, nullable=False)


class REGISTER_OC(db.Model):
    __tablename__ = 'REGISTER_OC'
    ID = db.Column(db.Integer, primary_key=True)
    NAME_CHECK = db.Column(db.String(50), db.ForeignKey('CHECKERS.NAME'))
    DATE_OPEN = db.Column(db.DateTime)
    DATE_CLOSE = db.Column(db.DateTime)
    AMOUNT_OPEN = db.Column(db.Integer)
    AMOUNT_CLOSE = db.Column(db.Integer)
    AMOUNT_TOTAL = db.Column(db.Integer)
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))


def add_checker(args=None, var=2):
    u = MYBUSINESS.query.filter_by(USERNAME=args['username']).first()
    nu = True
    if 'name' in args:
        c = CHECKERS(NAME=args['name'], SURNAME=args['surname'],
                     BIRTH_DAY=args['birthday'], ADDRESS=args['address'],
                     PHONE=args['phone'], EMAIL=args['email'], TYPE_USER=var,
                     BUSINESS_REF=u.USERNAME, PIN=args['pin'])
    else:
        c = CHECKERS(NAME='Tu nombre', SURNAME='Tu apellido',
                     BUSINESS_REF=u.USERNAME, TYPE_USER=1, PIN=ra())
        nu = False
    db.session.add(c)
    db.session.commit()
    return nu


def add_business(args):
    b = MYBUSINESS(USERNAME=args['username'], EMAIL=args['email'],
                   PASSWORD=lock(args['password']), TYPE_ACCOUNT=1)
    db.session.add(b)
    db.session.commit()
    add_checker(args)


def check_db_users(data):
    user = MYBUSINESS.query.filter_by(USERNAME=data['username']).first()
    if not user:
        email = MYBUSINESS.query.filter_by(EMAIL=data['email']).first()
        if not email:
            return True
        else:
            return False
    else:
        return False


def verify_user(args):
    query = MYBUSINESS.query.filter_by(USERNAME=args['username']).first()
    if query and check_password_hash(query.PASSWORD, args['password']):
        session["new_user"] = query.USERNAME
        return True
    else:
        return False


def create_user_dict(args) -> dict:
    key = ['Nombre de usuario', 'Email', 'Nombre fiscal', 'Nombre comercial', 'Teléfono', 'Dirección',
           'CUIT', 'IIBB', 'Fecha de inicio', 'Rubro', 'IVA', 'Cajeros', 'Creación de cuenta', 'Tipo de cuenta']
    val = args.TYPE_ACCOUNT
    type_user = TYPE_ACCOUNT.query.filter_by(ID=val).first()
    return {
        key[0]: args.USERNAME,
        key[1]: args.EMAIL,
        key[2]: args.FISCAL_NAME,
        key[3]: args.BUSINESS_NAME,
        key[4]: args.PHONE,
        key[5]: args.ADDRESS,
        key[6]: args.CUIT,
        key[7]: args.IIBB,
        key[8]: args.BEGIN_DATE,
        key[9]: args.ITEM,
        key[10]: args.IVA,
        key[11]: args.CHECKERS,
        key[12]: args.CREATE_AT,
        key[13]: type_user.TYPE,
    }


def create_checker_dict(args):
    key = ['Nombre', 'Apellido',
           ' Fecha de nacimiento', 'Domicilio', 'Teléfono', 'Email', 'Tipo', 'Pin de accesso']
    if args:
        return {
            key[0]: args.NAME,
            key[1]: args.SURNAME,
            key[2]: args.BIRTH_DAY,
            key[3]: args.ADDRESS,
            key[4]: args.PHONE,
            key[5]: args.EMAIL,
            key[6]: args.TYPE_USER,
            key[7]: args.PIN
        }
    else:
        return {
            key[0]: CHECK_DATA[0],
            key[1]: CHECK_DATA[1],
            key[2]: CHECK_DATA[2],
            key[3]: CHECK_DATA[3],
            key[4]: CHECK_DATA[4],
            key[5]: CHECK_DATA[5],
            key[6]: CHECK_DATA[6],
            key[7]: CHECK_DATA[7],

        }


@ app.before_request
def before_request():
    if 'new_user' in session:
        g.user = session['new_user']
    else:
        g.user = None
        g.check = None
    if 'open_check' in session:
        g.check = session['open_check']
    else:
        g.check = None


@ app.route('/')
def index():
    if g.user:
        return redirect(url_for('application'))
    else:
        return render_template('signup.html')


@ app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        if request.form['password'] == request.form['re-password']:
            if check_db_users(request.form):
                add_business(request.form)
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
    session.pop('open_check', None)
    flash("Se ha cerrado sesión con éxito", "success")
    return redirect(url_for('index'))


@app.route('/app')
def application():
    if g.user:
        check = CHECKERS.query.filter_by(BUSINESS_REF=g.user).all()
        if 'Tu nombre' in check[0].NAME:
            return render_template("check_login.html", change=True, data=create_checker_dict(None), admin=['Admin' if check[0].TYPE_USER == 1 else 'Cajero', check[0].PIN])
        else:
            if g.check:
                return redirect(url_for('sell'))
            else:
                return render_template("check_login.html", checkers=check)
    flash("Debes iniciar sesión primero", "danger")
    return redirect(url_for("index"))


@app.route('/app/admin')
def admin():
    if g.user:
        checks = CHECKERS.query.filter_by(BUSINESS_REF=g.user).all()
        user = create_user_dict(
            MYBUSINESS.query.filter_by(USERNAME=g.user).first())
        return render_template('admin.html', user=user, checkers=checks, data=DATA)
    flash("Debes iniciar sesión primero", "danger")
    return redirect(url_for("index"))


@app.route('/update/admin', methods=['POST'])
def update_admin():
    d = request.form
    ud = False
    try:
        if d['NAME']:
            u = CHECKERS.query.filter_by(BUSINESS_REF=g.user).first()
            u.NAME = d['NAME'] if u.NAME != d['NAME'] else u.NAME
            u.SURNAME = d['SURNAME'] if u.SURNAME != d['SURNAME'] else u.SURNAME
            u.BIRTH_DAY = d['BIRTH_DAY'] if u.BIRTH_DAY != d['BIRTH_DAY'] else u.BIRTH_DAY
            u.ADDRESS = d['ADDRESS'] if u.ADDRESS != d['ADDRESS'] else u.ADDRESS
            u.PHONE = d['PHONE'] if u.PHONE != d['PHONE'] else u.PHONE
            u.EMAIL = d['EMAIL'] if u.EMAIL != d['EMAIL'] else u.EMAIL
            ud = True
    except:
        c = CHECKERS.query.filter_by(NAME=g.check).first()
        if c.TYPE_USER == 1:
            u = MYBUSINESS.query.filter_by(USERNAME=g.user).first()
            u.EMAIL = d['EMAIL'] if u.EMAIL != d['EMAIL'] else u.EMAIL
            u.FISCAL_NAME = d['FISCAL_NAME'] if u.FISCAL_NAME != d['FISCAL_NAME'] else u.FISCAL_NAME
            u.BUSINESS_NAME = d['BUSINESS_NAME'] if u.BUSINESS_NAME != d['BUSINESS_NAME'] else u.BUSINESS_NAME
            u.PHONE = d['PHONE'] if u.PHONE != d['PHONE'] else u.PHONE
            u.ADDRESS = d['ADDRESS'] if u.ADDRESS != d['ADDRESS'] else u.ADDRESS
            u.CUIT = d['CUIT'] if u.CUIT != d['CUIT'] else u.CUIT
            u.IIBB = d['IIBB'] if u.IIBB != d['IIBB'] else u.IIBB
            u.BEGIN_DATE = d['BEGIN_DATE'] if u.BEGIN_DATE != d['BEGIN_DATE'] else u.BEGIN_DATE
            u.ITEM = d['ITEM'] if u.ITEM != d['ITEM'] else u.ITEM
            u.IVA = d['IVA'] if u.IVA != d['IVA'] else u.IVA
            ud = True
    finally:
        if ud:
            db.session.add(u)
            db.session.commit()
            flash("Cambios realizados con éxito", "success")
        else:
            flash("No tenes permisos para modificar esta sección", "warning")
        return redirect(url_for('application'))


@app.route('/login/checker', methods=['POST'])
def login_check():
    r = request.form
    c = CHECKERS.query.filter_by(BUSINESS_REF=g.user).filter_by(
        NAME=r['CHECKER']).filter_by(PIN=r['PIN']).first()
    if c:
        g.check = session['open_check'] = r['CHECKER']
        flash(f"Caja {g.check} está abierto", "success")
        return redirect(url_for('application'))
    flash("Pin ingresado es incorrecto, si olvidaste el Pin contactate con el administrador", "danger")
    return redirect(url_for('index'))


@app.route('/update/checker', methods=['POST'])
def update_checker():
    print(request.form)
    return redirect(url_for('index'))


@app.route('/logout/check')
def close_check():
    session.pop('open_check', None)
    return redirect(url_for('application'))


@app.route('/check')
def check():
    if g.check:
        return render_template("app.html", title='Caja')
    else:
        flash("Debes abrir caja primero", "warning")
        return redirect(url_for('application'))


@app.route('/sell')
def sell():
    if g.check:
        return render_template("app.html", title='Ventas')
    else:
        flash("Debes abrir caja primero", "warning")
        return redirect(url_for('application'))


@app.route('/clients')
def clients():
    if g.check:
        return render_template("app.html", title='Clientes')
    else:
        flash("Debes abrir caja primero", "warning")
        return redirect(url_for('application'))


@app.route('/provider')
def provider():
    if g.check:
        return render_template("app.html", title='Proveedores')
    else:
        flash("Debes abrir caja primero", "warning")
        return redirect(url_for('application'))


@app.route('/article')
def article():
    if g.check:
        return render_template("app.html", title='Artículos')
    else:
        flash("Debes abrir caja primero", "warning")
        return redirect(url_for('application'))


@app.route('/list')
def list():
    res = request.args
    print(res)
    if g.check:
        return render_template("app.html", title='Listas')
    else:
        flash("Debes abrir caja primero", "warning")
        return redirect(url_for('application'))


@app.route('/search')
def search():
    # res = request.full_path
    res = request.args
    print(res['item'])
    q = CHECKERS.query.filter_by(BUSINESS_REF=g.user).all()
    return render_template("app.html", title='Busqueda', q=q)


@app.route('/<string:user>')
@app.route('/<string:user>/<string:checker>')
@app.route('/<string:user>/<string:checker>/<string:action>')
def user(user=None, checker=None, action=None):
    if user == g.user:
        if checker == g.check:
            return redirect(url_for(g.user, checker=g.check, action='sell'))
        else:
            check = CHECKERS.query.filter_by(BUSINESS_REF=g.user).all()
            if 'Tu nombre' in check[0].NAME:
                return render_template("check_login.html", change=True, data=create_checker_dict(None), admin=['Admin' if check[0].TYPE_USER == 1 else 'Cajero', check[0].PIN])
            else:
                return render_template('check_login.html', checkers=check)
    else:
        flash("Debes iniciar sesión primero", "danger")
        return redirect(url_for('index'))


@app.errorhandler(404)
def error_handler(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.create_all()
    # try:
    #     db.session.add(TYPE_ACCOUNT(ID=1, TYPE='Free'))
    #     db.session.add(TYPE_ACCOUNT(ID=2, TYPE='Premium'))
    #     db.session.commit()
    # except error.IntegrityError:
    #     print("Some data is created")
    app.run(debug=True, port=8080)
