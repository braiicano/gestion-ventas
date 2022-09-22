from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"#direccion de ddbb


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),)
    email = db.Column(db.String(50),)
    password = db.Column(db.String(100),)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/singup", methods=['POST'])
def singup():
    return "Ingreso en singup"

@app.route("/login", methods=['GET'])
def login():
    return "Ingreso en login"

if __name__ == '__main__':
    db.create_all()
    app.run(debug= True, port= 5000)
