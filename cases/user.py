from flask import render_template,jsonify,request,url_for,redirect,session
from models import Cargo,db

def go_user(app):
    @app.route('/user')
    def user():
        return render_template('user.html')