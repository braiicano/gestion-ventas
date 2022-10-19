from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
# CONVERTIR LOS __repr__() en DICT para al llamarlo tener acceso a todos los valores
database = SQLAlchemy()

LINK_REGISTER = database.Table('LINK_REGISTER',
                               database.Column('CHECKER_ID', database.Integer, database.ForeignKey('CHECKERS.ID'),
                                               primary_key=True),
                               database.Column('REGISTER_OC_ID', database.Integer, database.ForeignKey(
                                   'REGISTER_OC.ID'), primary_key=True))


class Base(database.Model):
    __abstract__ = True
    ID = database.Column(database.Integer, primary_key=True)
    NAME = database.Column(database.String(50), nullable=False)
    SURNAME = database.Column(database.String(50), nullable=False)
    BIRTH_DAY = database.Column(database.String(255))
    ADDR_STREET = database.Column(database.String(50))
    ADDR_CITY = database.Column(database.String(50))
    ADDR_COUNTRY = database.Column(database.String(50))
    PHONE = database.Column(database.String(50))
    EMAIL = database.Column(database.String(50))
    DU = database.Column(database.Integer)
    LAST_UPDATE = database.Column(
        database.String, default=dt.today().strftime("%Y-%m-%d %H:%M:%S"))
    CREATED_AT = database.Column(
        database.String, default=dt.today().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self) -> str:
        self.DICT = {"ID": self.ID, "NAME": self.NAME, "SURNAME": self.SURNAME, "ADDR_STREET": self.ADDR_STREET,
                     "ADDR_CITY": self.ADDR_CITY, "ADDR_COUNTRY": self.ADDR_COUNTRY, "PHONE": self.PHONE,
                     "EMAIL": self.EMAIL, "DU": self.DU, "LAST_UPDATE": self.LAST_UPDATE, "CREATED_AT": self.CREATED_AT}
        return f"{self.DICT}"


class MYBUSINESS(database.Model):
    __nametable__ = 'MYBUSINESS'
    ID = database.Column(database.Integer, primary_key=True)
    USERNAME = database.Column(database.String(50), nullable=False)
    EMAIL = database.Column(database.String(50), nullable=False)
    PASSWORD = database.Column(database.String(100), nullable=False)
    PHONE = database.Column(database.String(50))
    ADDR_STREET = database.Column(database.String(50))
    ADDR_CITY = database.Column(database.String(50))
    ADDR_COUNTRY = database.Column(database.String(50))
    FISCAL_NAME = database.Column(database.String(50))
    BUSINESS_NAME = database.Column(database.String(50))
    CUIT = database.Column(database.Integer, unique=True)
    IIBB = database.Column(database.Float)
    BEGIN_TIME = database.Column(database.Date)
    ITEM = database.Column(database.String(50))  # In future is a list of items
    IVA = database.Column(database.Float)
    CREATED_AT = database.Column(
        database.DateTime, default=dt.today().strftime("%Y-%m-%d %H:%M:%S"))
    TYPE_ACCOUNT = database.Column(
        database.Integer, default=1)  # 1 is free / 2 is premium

    def __repr__(self) -> str:
        self.DICT = {"ID": self.ID, "USERNAME": self.USERNAME, "EMAIL": self.EMAIL, "ADDR_STREET": self.ADDR_STREET,
                     "ADDR_CITY": self.ADDR_CITY, "ADDR_COUNTRY": self.ADDR_COUNTRY, "PHONE": self.PHONE,
                     "EMAIL": self.EMAIL, "FISCAL_NAME": self.FISCAL_NAME, "BUSINESS_NAME": self.BUSINESS_NAME,
                     "CUIT": self.CUIT, "IIBB": self.IIBB, "BEGIN_TIME": self.BEGIN_TIME, "ITEM": self.ITEM,
                     "IVA": self.IVA, "TYPE_ACCOUNT": self.TYPE_ACCOUNT, "CREATED_AT": self.CREATED_AT}
        return f'{self.DICT}'


class INVOICE(database.Model):
    __nametable__ = 'INVOICE'
    ID = database.Column(database.Integer, primary_key=True)
    TYPE_INVOICE = database.Column(database.String(50))
    DATE = database.Column(database.Date)
    HOUR = database.Column(database.Time)
    TOTAL = database.Column(database.Numeric)
    ORDER_DETAILS = database.Column(database.String(50))
    BUSINESS_REF = database.Column(database.String(
        50), database.ForeignKey('CHECKERS.BUSINESS_REF'))
    CHECKER_ID = database.Column(
        database.Integer, database.ForeignKey('CHECKERS.ID'))
    CLIENT_ID = database.Column(
        database.Integer, database.ForeignKey('CLIENTS.ID'))
    # CHECKER_REL = database.relationship(
    #     'CHECKERS', backref=database.backref('INVOICE'))
    # CLIENT_REL = database.relationship(
    #     'CLIENTS', backref=database.backref('INVOICE', lazy=True))

    def __repr__(self) -> str:
        return f"{self.ID},{self.CHECKER_ID}"


class CHECKERS(Base):
    __nametable__ = 'CHECKERS'
    PIN = database.Column(database.Integer, nullable=False)
    # 1 is checker / 2 is admin
    TYPE_USER = database.Column(database.Integer, default=1)
    BUSINESS_REF = database.Column(
        database.String(50), database.ForeignKey('MYBUSINESS.USERNAME'))
    # BUSINESS_REL = database.relationship(
    #     'MYBUSINESS', backref=database.backref('CHECKERS', lazy=True))


class CLIENTS(Base):
    __nametable__ = 'CLIENTS'
    INVOICES = database.Column(database.Integer)
    BUSINESS_REF = database.Column(
        database.String(50), database.ForeignKey('MYBUSINESS.USERNAME'))
    # BUSINESS_REL_CLIENTS = database.relationship(
    #   'MYBUSINESS', backref=database.backref('CLIENTS', lazy=True))


class PROVIDERS(database.Model):
    __nametable__ = 'PROVIDERS'
    ID = database.Column(database.Integer, primary_key=True)
    NAME = database.Column(database.String(50))
    NAME_CONTACT = database.Column(database.String(50))
    ADDR_STREET = database.Column(database.String(50))
    ADDR_CITY = database.Column(database.String(50))
    ADDR_COUNTRY = database.Column(database.String(50))
    PHONE = database.Column(database.Integer)
    EMAIL = database.Column(database.String(50))
    CUIT = database.Column(database.Integer)
    BUSINESS_REF = database.Column(
        database.String(50), database.ForeignKey('MYBUSINESS.USERNAME'))
    # BUSINESS_REL = database.relationship(
    #     'MYBUSINESS', backref=database.backref('PROVIDERS', lazy=True))

    def __repr__(self) -> str:
        return f"{self.NAME}"


class ARTICLES(database.Model):
    __nametable__ = 'ARTICLES'
    ID = database.Column(database.Integer, primary_key=True)
    NAME = database.Column(database.String(50), nullable=False)
    CATEGORY = database.Column(database.String(50))
    PROVIDER = database.Column(
        database.Integer, database.ForeignKey('PROVIDERS.ID'))
    MAKER = database.Column(database.String(50))
    SKU = database.Column(database.String(50))
    STOCK = database.Column(database.Integer)
    COST = database.Column(database.Float)
    PUBLIC_PRICE = database.Column(database.Float)
    PROFIT = database.Column(database.Float)
    IVA = database.Column(database.Float)
    ACTIVE = database.Column(database.String(5))
    BUSINESS_REF = database.Column(
        database.String(50), database.ForeignKey('PROVIDERS.BUSINESS_REF'))
    # PROVIDER_REL = database.relationship(
    # 'PROVIDERS', backref=database.backref('ARTICLES', lazy=True), foreign_keys=('PROVIDER','BUSINESS_REF'))
    LAST_UPDATE = database.Column(
        database.DateTime, default=dt.today().strftime("%Y-%m-%d %H:%M:%S"))

    def __repr__(self) -> str:
        return f"{self.NAME}"


class ORDER_DETAILS(database.Model):
    __nametable__ = 'ORDER_DETAILS'
    ID = database.Column(database.Integer, primary_key=True)
    INVOICE_ID = database.Column(
        database.Integer, database.ForeignKey('INVOICE.ID'))
    ARTICLES_ID = database.Column(
        database.Integer, database.ForeignKey('ARTICLES.ID'))
    AMOUNT_ARTICLES = database.Column(database.Integer)
    PRICE_ARTICLES = database.Column(database.Numeric(16, 2))
    TOTAL_ORDER = database.Column(database.Numeric(16, 2))

    def __repr__(self) -> str:
        return f"{self.ID}"


class REGISTER_OC(database.Model):
    __nametable__ = 'REGISTER_OC'
    ID = database.Column(database.Integer, primary_key=True)
    OPEN_DATE = database.Column(database.String(30))
    OPEN_TIME = database.Column(database.String(30))
    OPEN_AMOUNT = database.Column(database.String(30))
    CLOSE_DATE = database.Column(database.String(30))
    CLOSE_TIME = database.Column(database.String(30))
    CLOSE_AMOUNT = database.Column(database.String(30))
    TOTAL_AMOUNT = database.Column(database.String(30))

    def __repr__(self) -> str:
        return f"{self.ID}"
