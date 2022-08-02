from http.client import FORBIDDEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from app import app, db
from app.model import Customer, Feedbacks, Facts, Admin, Ram, Gpu, Ssd, Psu, Cpu, Feedbacks, Casing, Customer, Mb, Pcpackage
import os
from sklearn.neighbors import DistanceMetric
dist = DistanceMetric.get_metric('hamming')

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.filter_by(id=user_id).first()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', message="WELCOME TO PALAMTECH PC BUILDER")

@app.route('/indexdefault')
def indexdefault():
    return render_template('index.html', message="WELCOME TO PALAMTECH PC BUILDER")

@app.route('/home')
def home():
    return render_template('home.html', message="WELCOME TO PALAMTECH PC BUILDER")