from flask import Flask
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
app.config['MySQL_PASSWORD'] = "password"
app.secret_key = "membuatLOginFlask1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/palamtech'
db = SQLAlchemy(app)

app.config.from_object('config')

from app import customerController
from app import staffController
from app import model
from app import view