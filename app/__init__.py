from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

# create database:
dbdir = "sqlite:///"+os.path.abspath(os.getcwd())+"/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable = False)

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/singup", methods=["GET","POST"])
def singup():
    if request.method == "POST":
        print(request.form)
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = Users(username=request.form["nickname"],email=request.form["email"],password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return "Registrado con exito"
    else:
        return "Usando metodo get"

@app.route("/login")
def login():
    print(request.form)
    return "Iniciando sesion"
# app.secret_key="Santino15Benicio19!"
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,port=8080)
