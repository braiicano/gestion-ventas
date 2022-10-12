from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randrange
from datetime import datetime as dt
import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

db = SQLAlchemy()


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
    LAST_UPDATE = db.Column(
        db.String, default=dt.today().strftime("%d-%m-%Y %H:%M:%S"))
    CREATED_AT = db.Column(
        db.String, default=dt.today().strftime("%d-%m-%Y %H:%M:%S"))


class ARTICLES(db.Model):
    __tablename__ = 'ARTICLES'
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50), nullable=False)
    CATEGORY = db.Column(db.String(50))
    PROVIDER = db.Column(db.String(50))
    MAKER = db.Column(db.String(50))
    SKU = db.Column(db.String(50))
    STOCK = db.Column(db.Integer)
    COST = db.Column(db.Integer)
    PUBLIC_PRICE = db.Column(db.Integer)
    IVA = db.Column(db.Integer, default=0)
    ACTIVE = db.Column(db.String(5))  # where 0=no active, 1=active
    LAST_UPDATE = db.Column(
        db.String, default=dt.today().strftime("%d-%m-%Y %H:%M:%S"))
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))
    #IMAGE = db.Column(db.BLOB)


class CHECKERS(BASE):
    __tablename__ = 'CHECKERS'
    TYPE_USER = db.Column(db.Integer, nullable=False,
                          default=2)  # If 1=admin,2=check
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))
    PIN = db.Column(db.Integer, nullable=False, default=ra())


class CLIENTS(BASE):
    __tablename__ = 'CLIENTS'
    INVOICES = db.Column(db.Integer, db.ForeignKey('INVOICE.ID'))
    DU = db.Column(db.Integer)
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))


class INVOICE(db.Model):
    __tablename__ = 'INVOICE'
    ID = db.Column(db.Integer, primary_key=True)
    TYPE_INVOICE = db.Column(db.String, nullable=False)
    DATE = db.Column(
        db.String, default=dt.today().strftime("%d-%m-%Y"))
    HOUR = db.Column(db.String, default=dt.today().strftime("%H:%M:%S"))
    TOTAL = db.Column(db.Integer)
    ORDER_DETAILS = db.Column(db.String(255))
    NAME_CHECKER = db.Column(db.Integer, db.ForeignKey('CHECKERS.ID'))
    NAME_CLIENTS = db.Column(db.String)


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
    # CHECKERS = db.Column(db.Integer)
    CREATE_AT = db.Column(
        db.String, default=dt.today().strftime("%d-%m-%Y %H:%M:%S"))
    TYPE_ACCOUNT = db.Column(db.Integer, default=1)  # 1 is free, 2 is premium


class ORDER_DETAILS(db.Model):
    __tablename__ = 'ORDER_DETAILS'
    ID = db.Column(db.Integer, primary_key=True)
    ID_INVOICE = db.Column(db.Integer, db.ForeignKey('INVOICE.ID'))
    AMOUNT = db.Column(db.Integer)
    ARTICLE_COST = db.Column(db.Integer)
    TOTAL_ORDER = db.Column(db.Integer)
    ID_ARTICLE = db.Column(db.Integer, db.ForeignKey('ARTICLES.ID'))


class PROVIDERS(db.Model):
    __tablename__ = 'PROVIDERS'
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50), nullable=False)
    NAME_CONTACT = db.Column(db.String(50))
    ADDRESS = db.Column(db.String(50))
    PHONE = db.Column(db.Integer)
    EMAIL = db.Column(db.String(50))
    BUSINESS_NAME = db.Column(db.String(50))
    BUSINESS_REF = db.Column(
        db.String(50), db.ForeignKey('MYBUSINESS.USERNAME'))


class REGISTER_OC(db.Model):
    __tablename__ = 'REGISTER_OC'
    ID = db.Column(db.Integer, primary_key=True)
    NAME_CHECK = db.Column(db.Integer, db.ForeignKey('CHECKERS.ID'))
    DATE_OPEN = db.Column(db.String)
    HOUR_OPEN = db.Column(db.String)
    AMOUNT_OPEN = db.Column(db.Integer)
    DATE_CLOSE = db.Column(db.String)
    HOUR_CLOSE = db.Column(db.String)
    AMOUNT_CLOSE = db.Column(db.Integer)
    AMOUNT_TOTAL = db.Column(db.Integer)
    BUSINESS_REF = db.Column(db.String, db.ForeignKey('MYBUSINESS.USERNAME'))


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
        return True
    else:
        return False


def create_user_dict(args) -> dict:
    key = ['Nombre de usuario', 'Email', 'Nombre fiscal', 'Nombre comercial', 'Teléfono', 'Dirección',
           'CUIT', 'IIBB', 'Fecha de inicio', 'Rubro', 'IVA', 'Creación de cuenta', 'Tipo de cuenta']
    val = args.TYPE_ACCOUNT
    type_user = 'Free' if val == 1 else 'Premium'

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
        key[11]: args.CREATE_AT,
        key[12]: type_user,
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
