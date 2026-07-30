from models import Faq_User
from flask import render_template, request, redirect, url_for
from app import db

def register_routes(app,db):
    @app.route("/", methods =["GET","POST"])
    def index():
        return render_template("index.html")
    @app.route("/edit", methods =["GET"])
    def edit():
        return render_template("edit.html")
    @app.route("/add_faq", methods =["POST"])
    def add_faq():
        
        return render_template("edit.html")
    @app.route("/delete_faq", methods =["DELETE"])
    def delete_faq():
        return render_template("edit.html")
