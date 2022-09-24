# Modules
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, make_response, session, escape, flash, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# Database directory connect
import os
dbdir = "sqlite:///" + \
    os.path.abspath(os.getcwd()) + "/database.db"  # direccion de ddbb

# App config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Class to create databases


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.now())
    # status = db.Column(db.Integer, nullable=False)


class Create_Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# CRUD


def create(data):
    hashed_pw = generate_password_hash(data['password'], method='sha256')
    new_user = Users(
        username=data['username'], email=data['email'], password=hashed_pw)  # ,status=1)
    db.session.add(new_user)
    db.session.commit()


def check_data(data, value):
    to_check = db.session.query(Users).all()
    for i in to_check:
        if data[value] == i.username or data[value] == i.email:
            return True
    return False


def showme():
    queries = db.session.query(Users).all()
    print(queries)


def update(data):
    pass


def delete(data):
    pass


def checker(data):
    user = Users.query.filter_by(username=data['username']).first()
    try:
        if user and check_password_hash(user.password, data['password']):
            return True
        else:
            return False
    except:
        return False

# App functions


@app.before_request
def before_request():
    if "new_session" in session:
        g.user = session['new_session']
    else:
        g.user = None


@app.route("/")
def index():
    try:
        if session['new_session'] != None:
            return redirect(url_for('home'))
    except:
        return render_template("index.html")


@app.route("/singup", methods=['POST'])
def singup():
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm-password']:
            if not check_data(request.form, 'username'):
                if not check_data(request.form, 'email'):
                    create(request.form)
                    session['new_session'] = request.form['username']
                    return redirect(url_for('home'))
                else:
                    flash('El email ya se encuentra registrado.', 'alert-message')
                    return redirect('/')
            else:
                flash('El usuario "{}" ya existe, elige otro nombre.'.format(
                    request.form['username']), 'alert-message')
                return redirect('/')
        else:
            flash('Las contraseñas no coinciden.', 'alert-message')
            return redirect('/')
    else:
        return redirect("error")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if checker(request.form):
            session['new_session'] = request.form['username']
            return redirect(url_for('home'))
        else:
            flash(
                "Error en credenciales, usuario y/o contraseña son invalidos", 'alert-message')
            return redirect("/")
    else:
        return redirect('/')


@app.route("/home")
def home():
    if g.user:
        iterable = request.args.get('name')
        queries = db.session.query(Users).all()
        if not iterable:
            return render_template('app.html', name=g.user, db=queries)
        return render_template(f'{iterable}.html', name=g.user, articles=temp_list, columns=ARTICLE_ELEMENTS, db= queries)
    else:
        flash("Debes iniciar sesión primero.", "alert-message")
        return redirect('/')


# agregar plantilla para creacion de articulos
@app.route("/article_new", methods=['POST'])
def article_new():
    temp_list[request.form['name']] = list()
    for article in request.form:
        temp_list[request.form['name']].append(request.form[article])
    print(temp_list)
    return redirect(url_for('home', name='article'))


@app.route("/search")  # mostrar vista de elemento encontrado o no
def search():
    # realizar consulta
    return redirect(url_for('home', name='article'))


@app.errorhandler(404)
def error(e):
    return render_template("error.html"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return redirect('error')


@app.route('/logout')
def logout(name='new_session'):
    session.pop(name, None)
    flash("Sesión cerrada correctamente", "leave-session")
    return redirect('/')


app.secret_key = "Santino2015Benicio19"
if __name__ == '__main__':
    db.create_all()
    temp_list = dict()
    ARTICLE_ELEMENTS = ['Nombre', 'Categoría', 'Proveedor', 'SKU', 'Stock',
                        'Precio', 'IVA', 'Ganancia', 'Promo', 'En venta', 'Descripción']
    app.run(debug=True, port=8000)
