from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"#direccion de ddbb


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/singup", methods=['GET','POST'])
def singup():
    if request.method == 'POST':
        print(request.form)
        return "Ingreso en singup"
    else:
        return redirect("error")

@app.route("/login", methods=['GET'])
def login():
    return "Ingreso en login"

@app.errorhandler(404)
def error(e):
    return render_template("error.html"),404


if __name__ == '__main__':
    db.create_all()
    app.run(debug= True, port= 5000)
