from flask import Flask, render_template, url_for, request, jsonify
from datetime import datetime
import pyrebase

@app.route("/")                             # Landing Page
def index():
    return render_template("index.html")

@app.route("/register")                     # Account Registration Page
def register():
    return render_template("register.html")

@app.route("/signIn")                       # Sign In Page
def signIn():
    return render_template("signIn.html")
