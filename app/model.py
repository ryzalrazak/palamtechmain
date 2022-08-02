from app import db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

class Customer(db.Model, UserMixin):
    customer = "parents"
    id = db.Column(db.Integer, primary_key=True)
    custEmail = db.Column(db.String(255), unique=True)
    custName = db.Column(db.String(255))
    custPhoneNo = db.Column(db.String(255))
    custAdd = db.Column(db.String(255))
    custPass = db.Column(db.String(255))
    childrens = db.relationship("child", backref="parents"),
    cascade = "all, delete"
   #customer = db.relationship('Customer', backref='feedback', lazy=True)

    def __init__(self, custEmail, custName, custPhoneNo, custAdd, custPass):
        self.custEmail = custEmail
        self.custName = custName
        self.custPhoneNo = custPhoneNo
        self.custAdd = custAdd
        self.custPass = custPass




class Admin(db.Model):
    adminID = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(255))
    adminEmail = db.Column(db.String(255), unique=True)
    adminPass = db.Column(db.String(255))

    def __init__(self, adminName, adminEmail, adminPass):
        self.adminName = adminName
        self.adminEmail = adminEmail
        self.adminPass = adminPass


class Feedbacks(db.Model):
    feedbacks = "children"
    fbID = db.Column(db.Integer, primary_key=True)
    custEmail = db.Column(db.String, db.ForeignKey('customer.custEmail'),
                          nullable=False)
    fbDate = db.Column(db.DateTime)
    fbType = db.Column(db.String(255))
    fbDesc = db.Column(db.String(255))

    def __init__(self, custEmail, fbType, fbDate, fbDesc):

        self.custEmail = custEmail
        self.fbType = fbType
        self.fbDate = fbDate
        self.fbDesc = fbDesc

class Casing(db.Model):
    casing = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price


class Mb(db.Model):
    mb = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price


class Gpu(db.Model):
    gpu = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price


class Ram(db.Model):
    ram = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price


class Ssd(db.Model):
    ssd = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price


class Psu(db.Model):
    psu = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price


class Cpu(db.Model):
    cpu = "children"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    price = db.Column(db.Float())

    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price

class Facts(db.Model):
    facts = "children"
    id = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.String, db.ForeignKey('customer.id'),
                          nullable=False)
    pricerange = db.Column(db.String(255))
    brandprefer = db.Column(db.String(255))
    reason = db.Column(db.String(255))
    color = db.Column(db.String(255))
    performance = db.Column(db.String(255))
    

    def __init__(self, custID, pricerange, brandprefer,reason,color,performance):
        self.custID = custID
        self.pricerange = pricerange
        self.brandprefer = brandprefer
        self.reason = reason
        self.color = color
        self.performance = performance

class Pcpackage(db.Model):
    pcpackage = "children"
    id = db.Column(db.Integer, primary_key=True)
    casing = db.Column(db.Integer, db.ForeignKey("casing.id"),
                       nullable=False)
    mb = db.Column(db.Integer, db.ForeignKey("mb.id"),
                   nullable=False)
    gpu = db.Column(db.Integer, db.ForeignKey("gpu.id"),
                    nullable=False)
    ram = db.Column(db.Integer, db.ForeignKey("ram.id"),
                    nullable=False)
    ssd = db.Column(db.Integer, db.ForeignKey("ssd.id"),
                    nullable=False)
    psu = db.Column(db.Integer, db.ForeignKey("psu.id"),
                    nullable=False)
    cpu = db.Column(db.Integer, db.ForeignKey("gpu.id"),
                    nullable=False)
    reason = db.Column(db.String(255))
    color = db.Column(db.String(255))
    performance = db.Column(db.String(255))

    def __init__(self, casing, mb, gpu, ram, ssd, psu, cpu,reason,color,performance):

        self.casing = casing
        self.mb = mb
        self.gpu = gpu
        self.ram = ram
        self.ssd = ssd
        self.psu = psu
        self.cpu = cpu
        self.reason = reason
        self.color = color
        self.performance = performance