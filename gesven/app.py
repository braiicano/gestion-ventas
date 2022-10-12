from flask import Flask, render_template, redirect, url_for, flash, request, g, session
from tables import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'mysecretkey'


@ app.before_request
def before_request():
    print(request.path)
    print(session)
    # print(g.idOpen)
    # print(g.type)
    if 'new_user' in session:
        g.user = session['new_user']
    else:
        g.user = None
        g.check = None
        g.idOpen = None
        g.type = None
    if 'checker' in session:
        g.check = session['checker']
    else:
        g.check = None
    if 'idOpen' in session:
        g.idOpen = session['idOpen']
    else:
        g.idOpen = None
    if 'type' in session:
        g.type = session['type']
    else:
        g.type = None


@ app.route('/')
def index():
    if g.user:
        return redirect(url_for('User', user=g.user))
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
                session["new_user"] = request.form['USERNAME']
                return redirect(url_for('index'))
            flash("Usuario y/o contraseña no son correctos", "danger")
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('new_user', None)
    session.pop('checker', None)
    session.pop('idOpen', None)
    session.pop('type', None)
    flash("Se ha cerrado sesión con éxito", "success")
    return redirect(url_for('index'))


@app.route('/admin/<string:option>', methods=['POST'])
def admin(option):
    if option == 'update':
        d = request.form
        ud = False
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
        if ud:
            db.session.add(u)
            db.session.commit()
            flash("Cambios realizados con éxito", "success")
        else:
            flash("No tenes permisos para modificar esta sección", "warning")
        return redirect(url_for('index'))


@app.route('/checker/<string:option>', methods=['GET', 'POST'])
def checker(option='logout'):
    if option == 'login' and request.method == 'POST':
        r = request.form
        print(r)
        if r['CHECKER']:
            name = r['CHECKER'].split('/')[0]
            surname = r['CHECKER'].split('/')[1]
            c = CHECKERS.query.filter_by(BUSINESS_REF=g.user).filter_by(
                NAME=name).filter_by(SURNAME=surname).filter_by(PIN=r['PIN']).first()
            if c:
                g.check = session['checker'] = name
                g.type = session['type'] = c.TYPE_USER
                return redirect(url_for('User', user=g.user, checker=g.check, action='check'))
            flash(
                "Pin ingresado es incorrecto, si olvidaste el Pin contactate con el administrador", "danger")
        else:
            flash("No seleccionó usuario", "warning")
        return redirect(url_for('index'))
    if option == 'logout' and request.method == 'GET':
        session.pop('checker', None)
        return redirect(url_for('index'))
    if option == 'open' and request.method == 'POST':
        r = request.form
        if g.idOpen:
            flash("Ya abrió caja", "danger")
        else:
            qoc = REGISTER_OC.query.filter_by(
                NAME_CHECK=g.check).filter_by(BUSINESS_REF=g.user).all()
            try:
                if qoc[-1].AMOUNT_CLOSE:
                    q = REGISTER_OC(NAME_CHECK=g.check, DATE_OPEN=dt.today().strftime("%d-%m-%Y"), HOUR_OPEN=dt.today().strftime("%H:%M:%S"),
                                    AMOUNT_OPEN=r['open'], BUSINESS_REF=g.user)
                    db.session.add(q), db.session.commit()
                    g.idOpen = session['idOpen'] = q.ID
                    flash("Caja abierta con éxito", "success")
                else:
                    g.idOpen = session['idOpen'] = qoc[-1].ID
            except IndexError:
                q = REGISTER_OC(NAME_CHECK=g.check, DATE_OPEN=dt.today().strftime("%d-%m-%Y"), HOUR_OPEN=dt.today().strftime("%H:%M:%S"),
                                AMOUNT_OPEN=r['open'], BUSINESS_REF=g.user)
                db.session.add(q), db.session.commit()
                g.idOpen = session['idOpen'] = q.ID
                flash("Caja abierta con éxito", "success")
        return redirect(url_for('index'))
    if option == 'close' and request.method == 'POST':
        r = request.form
        if g.idOpen:
            q = REGISTER_OC.query.filter_by(ID=g.idOpen).first()
            q.DATE_CLOSE = dt.today().strftime("%d-%m-%Y")
            q.HOUR_CLOSE = dt.today().strftime("%H:%M:%S")
            q.AMOUNT_CLOSE = r['close']
            q.AMOUNT_TOTAL = float(r['close']) - q.AMOUNT_OPEN
            db.session.add(q), db.session.commit()
            session.pop('idOpen', None)
            flash("Caja cerró con éxito", "success")
        else:
            flash("No se abrió caja aún", "warning")
        return redirect(url_for('index'))
    if option == 'edit' and request.method == 'POST':
        a = request.args['values']
        r = request.form
        q = CHECKERS.query.filter_by(ID=a).first()
        q.NAME = r['NAME'] if q.NAME != r['NAME'] else q.NAME
        q.SURNAME = r['SURNAME'] if q.SURNAME != r['SURNAME'] else q.SURNAME
        q.BIRTH_DAY = r['BIRTH_DAY'] if q.BIRTH_DAY != r['BIRTH_DAY'] else q.BIRTH_DAY
        q.ADDRESS = r['ADDRESS'] if q.ADDRESS != r['ADDRESS'] else q.ADDRESS
        q.PHONE = r['PHONE'] if q.PHONE != r['PHONE'] else q.PHONE
        q.EMAIL = r['EMAIL'] if q.EMAIL != r['EMAIL'] else q.EMAIL
        q.PIN = r['PIN'] if q.PIN != r['PIN'] else q.PIN
        db.session.add(q)
        db.session.commit()
        if g.check != q.NAME:
            session['checker'] = q.NAME
        flash("Datos actualizados", "success")
    if option == 'new' and request.method == 'POST':
        r = request.form
        q = CHECKERS(NAME=r['NAME'], SURNAME=r['SURNAME'], BIRTH_DAY=r['BIRTH_DAY'],
                     ADDRESS=r['ADDRESS'], PHONE=r['PHONE'], EMAIL=r['EMAIL'], PIN=r['PIN'], BUSINESS_REF=g.user)
        db.session.add(q)
        db.session.commit()
        flash("Nuevo cajero registrado", "success")
    if option == 'delete':
        q = CHECKERS.query.filter_by(BUSINESS_REF=g.user).filter_by(
            ID=request.args['values']).first()
        db.session.delete(q)
        db.session.commit()
        flash("Cajero %s fué eliminado" % q.NAME, "danger")
    if option == 'admin' and request.method == 'POST':
        a = request.args
        r = request.form
        ud = False
        if a['values'] == 'create':
            c = CHECKERS.query.filter_by(BUSINESS_REF=g.user).first()
            c.NAME = r['NAME'] if c.NAME != r['NAME'] else c.NAME
            c.SURNAME = r['SURNAME'] if c.SURNAME != r['SURNAME'] else c.SURNAME
            c.BIRTH_DAY = r['BIRTH_DAY'] if c.BIRTH_DAY != r['BIRTH_DAY'] else c.BIRTH_DAY
            c.ADDRESS = r['ADDRESS'] if c.ADDRESS != r['ADDRESS'] else c.ADDRESS
            c.PHONE = r['PHONE'] if c.PHONE != r['PHONE'] else c.PHONE
            c.EMAIL = r['EMAIL'] if c.EMAIL != r['EMAIL'] else c.EMAIL
            g.check = session['checker'] = r['NAME']
            ud = True
        elif a['values'] == 'update':
            ud = True
        if ud:
            db.session.add(c)
            db.session.commit()
            flash("Se actualizó con éxito", "success")
        else:
            flash("Ocurrió un error al cargar los datos", 'danger')
    return redirect(url_for('User', user=g.user, checker=g.check, action='sell'))


@app.route('/client/<string:option>', methods=['POST', 'GET'])
def client(option):
    ud = False
    r = request.form
    if option == 'new' and request.method == 'POST':
        c = CLIENTS(NAME=r['NAME'], SURNAME=r['SURNAME'], BIRTH_DAY=r['BIRTH_DAY'], ADDRESS=r['ADDRESS'],
                    PHONE=r['PHONE'], EMAIL=r['EMAIL'], DU=r['DOCUMENT'], BUSINESS_REF=g.user)
        ud = True
    if option == 'edit' and request.method == 'POST':
        a = request.args['values']
        c = CLIENTS.query.filter_by(ID=a).first()
        print(a, c)
        c.DU = r['DOCUMENT'] if c.DU != r['DOCUMENT'] else c.DU
        c.NAME = r['NAME'] if c.NAME != r['NAME'] else c.NAME
        c.SURNAME = r['SURNAME'] if c.SURNAME != r['SURNAME'] else c.SURNAME
        c.BIRTH_DAY = r['BIRTH_DAY'] if c.BIRTH_DAY != r['BIRTH_DAY'] else c.BIRTH_DAY
        c.ADDRESS = r['ADDRESS'] if c.ADDRESS != r['ADDRESS'] else c.ADDRESS
        c.PHONE = r['PHONE'] if c.PHONE != r['PHONE'] else c.PHONE
        c.EMAIL = r['EMAIL'] if c.EMAIL != r['EMAIL'] else c.EMAIL
        g.check = session['checker'] = r['NAME']
        ud = True
    if option == 'delete' and request.method == 'GET':
        a = request.args['values']
        c = CLIENTS.query.filter_by(ID=a).first()
        db.session.delete(c)
        db.session.commit()
    if ud:
        db.session.add(c)
        db.session.commit()
        flash("Cambios realizados con éxito", "success")

    return redirect(url_for('User', user=g.user, checker=g.check, action='clients'))


@app.route('/provider/<string:option>', methods=['POST', 'GET'])
def provider(option):
    ud = False
    r = request.form
    if option == 'new' and request.method == 'POST':
        c = PROVIDERS(NAME=r['NAME'], NAME_CONTACT=r['NAME_CONTACT'], BUSINESS_NAME=r['BUSINESS_NAME'], ADDRESS=r['ADDRESS'],
                      PHONE=r['PHONE'], EMAIL=r['EMAIL'], BUSINESS_REF=g.user)
        ud = True
    if option == 'edit' and request.method == 'POST':
        a = request.args['values']
        c = PROVIDERS.query.filter_by(ID=a).first()
        c.NAME = r['NAME'] if c.NAME != r['NAME'] else c.NAME
        c.NAME_CONTACT = r['NAME_CONTACT'] if c.NAME_CONTACT != r['NAME_CONTACT'] else c.NAME_CONTACT
        c.BUSINESS_NAME = r['BUSINESS_NAME'] if c.BUSINESS_NAME != r['BUSINESS_NAME'] else c.BUSINESS_NAME
        c.ADDRESS = r['ADDRESS'] if c.ADDRESS != r['ADDRESS'] else c.ADDRESS
        c.PHONE = r['PHONE'] if c.PHONE != r['PHONE'] else c.PHONE
        c.EMAIL = r['EMAIL'] if c.EMAIL != r['EMAIL'] else c.EMAIL
        ud = True
    if option == 'delete' and request.method == 'GET':
        a = request.args['values']
        c = PROVIDERS.query.filter_by(ID=a).first()
        db.session.delete(c)
        db.session.commit()
    if ud:
        db.session.add(c)
        db.session.commit()
        flash("Cambios realizados con éxito", "success")

    return redirect(url_for('User', user=g.user, checker=g.check, action='providers'))


@app.route('/article/<string:option>', methods=['POST', 'GET'])
def article(option):
    ud = False
    r = request.form
    if option == 'new' and request.method == 'POST':
        try:
            val = r['ACTIVE']
        except KeyError:
            val = 'off'
        c = ARTICLES(NAME=r['NAME'], CATEGORY=r['CATEGORY'], PROVIDER=r['PROVIDER'], MAKER=r['MAKER'],
                     SKU=r['SKU'], STOCK=r['STOCK'], COST=r['COST'], PUBLIC_PRICE=r['PUBLIC_PRICE'], IVA=r['IVA'], ACTIVE=val, LAST_UPDATE=dt.today().strftime("%d-%m-%Y %H:%M:%S"), BUSINESS_REF=g.user)
        ud = True
    if option == 'edit' and request.method == 'POST':
        a = request.args['values']
        c = ARTICLES.query.filter_by(ID=a).first()
        c.NAME = r['NAME'] if c.NAME != r['NAME'] else c.NAME
        c.CATEGORY = r['CATEGORY'] if c.CATEGORY != r['CATEGORY'] else c.CATEGORY
        c.PROVIDER = r['PROVIDER'] if c.PROVIDER != r['PROVIDER'] else c.PROVIDER
        c.MAKER = r['MAKER'] if c.MAKER != r['MAKER'] else c.MAKER
        c.SKU = r['SKU'] if c.SKU != r['SKU'] else c.SKU
        c.STOCK = r['STOCK'] if c.STOCK != r['STOCK'] else c.STOCK
        c.COST = r['COST'] if c.COST != r['COST'] else c.COST
        c.PUBLIC_PRICE = r['PUBLIC_PRICE'] if c.PUBLIC_PRICE != r['PUBLIC_PRICE'] else c.PUBLIC_PRICE
        c.IVA = r['IVA'] if c.IVA != r['IVA'] else c.IVA
        c.ACTIVE = r['ACTIVE'] if c.ACTIVE != r['ACTIVE'] else c.ACTIVE
        c.LAST_UPDATE = dt.today().strftime("%d-%m-%Y %H:%M:%S")
        ud = True
    if option == 'delete' and request.method == 'GET':
        a = request.args['values']
        c = ARTICLES.query.filter_by(ID=a).first()
        db.session.delete(c)
        db.session.commit()
    if ud:
        db.session.add(c)
        db.session.commit()
        flash("Cambios realizados con éxito", "success")

    return redirect(url_for('User', user=g.user, checker=g.check, action='articles'))


def admin_check(user):
    u = CHECKERS.query.filter_by(
        BUSINESS_REF=g.user).filter_by(NAME=user).first()
    if u.TYPE_USER == 1:
        return True
    else:
        return False


@app.route('/csv/upload/<string:section>', methods=['POST'])
def upload_csv(section):
    if section == 'clients':
        csv = request.files['csv-file']
        # filecsv = secure_filename(csv.filename)
        # csv = csv.save(app.config['UPLOAD_FOLDER']+filecsv)
        temp = csv.stream.readlines()  # .decode()
        l = []
        if len(temp) > 0:
            for a in temp:
                q = CLIENTS()
                d = a.decode()
                q.DU = d.split(',')[0]
                q.NAME = d.split(',')[1]
                q.SURNAME = d.split(',')[2]
                q.PHONE = d.split(',')[3]
                q.BUSINESS_REF = g.user
                db.session.add(q)
            db.session.commit()

        else:
            flash("No seleccionó archivo para subir", "info")
    return redirect(url_for('User', user=g.user, checker=g.check, action=section))


@app.route('/app/<string:user>')
@app.route('/app/<string:user>/<string:checker>')
@app.route('/app/<string:user>/<string:checker>/<string:action>')
def User(user=None, checker=None, action=None):
    # print(g.user, g.check, action)
    if user == g.user and g.user:
        if checker == g.check and g.check:
            if action:
                if action == 'sell':
                    openAt = None
                    if g.idOpen:
                        openAt = REGISTER_OC.query.filter_by(
                            ID=g.idOpen).first().HOUR_OPEN
                    return render_template("application/sells.html", openAt=openAt)
                if action == 'admin':
                    if admin_check(g.check):
                        return render_template('application/admin.html', user=create_user_dict(
                            MYBUSINESS.query.filter_by(USERNAME=g.user).first()), checkers=CHECKERS.query.filter_by(BUSINESS_REF=g.user).all(), data=DATA, randomPin=ra())
                    else:
                        flash(
                            "No tenes permisos suficientes para esta función", "warning")
                        return redirect(url_for('User', user=g.user, checker=g.check, action='sell'))
                if action == 'check':
                    ocheck = REGISTER_OC.query.filter_by(ID=g.idOpen).first()
                    c = CHECKERS.query.filter_by(BUSINESS_REF=g.user).all()
                    roc = REGISTER_OC.query.filter_by(BUSINESS_REF=g.user).filter_by(
                        DATE_OPEN=dt.today().strftime("%d-%m-%Y")).all()
                    print(roc)
                    return render_template("application/checkers.html", ocheck=ocheck, checkers=c, today_check=roc)
                if action == 'clients':
                    lc = CLIENTS.query.filter_by(BUSINESS_REF=g.user).all()
                    print(lc)
                    return render_template("application/clients.html", list_clients=lc)
                if action == 'providers':
                    lp = PROVIDERS.query.filter_by(BUSINESS_REF=g.user).all()
                    return render_template("application/providers.html", list_providers=lp)
                if action == 'articles':
                    la = ARTICLES.query.filter_by(BUSINESS_REF=g.user).all()
                    return render_template("application/articles.html", list_articles=la)
                if action == 'list':
                    print(request.args)
                    return render_template("application/list.html")
                if action == 'modify':
                    q = CHECKERS.query.filter_by(
                        BUSINESS_REF=g.user).filter_by(NAME=g.check).first()
                    return render_template("application/modify.html", user=q)
            else:
                if request.path == ('/app/'+g.user+'/'+g.check):
                    return render_template("app.html")
                else:
                    return redirect(url_for('User', user=g.user, checker=g.check, action='sell'))
        else:
            check = CHECKERS.query.filter_by(BUSINESS_REF=g.user).all()
            if 'Tu nombre' in check[0].NAME:
                return render_template("check_login.html", change=True, data=create_checker_dict(None), admin=['Admin' if check[0].TYPE_USER == 1 else 'Cajero', check[0].PIN])
            else:
                if g.check:
                    return redirect(url_for('User', user=g.user, checker=g.check, action='sell'))
                else:
                    if request.args:
                        flash("Debes iniciar con pin para acceder", "warning")
                    return render_template('check_login.html', checkers=check)
    else:
        if g.user:
            return render_template('error.html')
        else:
            flash("Debes iniciar sesión primero", "danger")
            return redirect(url_for('index'))


@app.errorhandler(404)
def error_handler(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.__init__(app)
    db.create_all()
    app.run(debug=True, port=5500)
