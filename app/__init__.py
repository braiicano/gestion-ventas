from flask import Flask, render_template, request, redirect
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
    password = db.Column(db.String(90), nullable = False)
class Checkers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.Integer)
    first_name =  db.Column(db.String(30), nullable = False)
    last_name =  db.Column(db.String(30), nullable = False)
    checker_email = db.Column(db.String(50))
    checker_pw = db.Column(db.String(90), nullable = False)


# response 
@app.route("/")
def index():
    return render_template('login.html')

@app.route("/singup", methods=["GET","POST"])
def singup():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        new_user = Users(username=request.form["nickname"],email=request.form["email"],password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return "Registrado con exito"
    else:
        return page_not_found(404)

@app.route("/login", methods=["POST"])
def login():
    print(request.form)
    hashed_pw = generate_password_hash(request.form["password"], method="sha256")
    search = Users(username=request.form["nickname"],password=hashed_pw)
    print(search)
    return redirect("/app")

@app.route("/app")
def gesven():
    return "iniciando sesion"
# app.secret_key="Santino15Benicio19!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',style='error')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,port=8080)
