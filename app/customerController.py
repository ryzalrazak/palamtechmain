from http.client import FORBIDDEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from app import app, db
from app.model import Customer, Feedbacks, Facts
import os
from sklearn.neighbors import DistanceMetric
dist = DistanceMetric.get_metric('hamming')

@app.route('/recommendation/<casing>/<mb>/<gpu>/<ram>/<ssd>/<psu>/<cpu>/<price>/<similarity>'
           , methods=['GET', 'POST'])
def recommendation(casing,mb,gpu,
                    ram,ssd,psu,
                    cpu,price,similarity):

    if request.method == 'POST':

        return redirect(url_for("question"))
    else:

        parm = {'casing': casing,
                'mb': mb,
                'gpu': gpu,
                'ram': ram,
                'ssd': ssd,
                'psu': psu,
                'cpu': cpu,
                'price': price,
                'similarity':similarity}
        

        return render_template("recommendation.html",**parm)

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        try:
            
            
            dic = {"price" : {'Less than 3000':0,"3000-5000":1,"above 5000":2},
                   "brand" : {"AMD":0,"INTEL":1},

                   "color" : {"Black":0,"White":1},

                   }

            ls_reason = ["Gaming",
                                "Streaming",
                                "Editing",
                                "Office Use"]

            ls_perf = ["Large memory",
                       "Fast render",
                       "Smooth gaming"]

            custID = request.form['id']
            price = request.form['price']
            brand =  request.form['brand']
            reason =  request.form.getlist('reason')
            color = request.form['color']
            perfomance = request.form.getlist('performance')
            

            
  
            # using list comprehension
            reasontodb = ' '.join([str(elem) for elem in reason])
            
            print(reasontodb) 
            performancetodb = ' '.join([str(elem) for elem in perfomance])
            
            print(performancetodb)
            

            creteria_to_take = []
            ls = []

            user_feat = []



            if price!="Don't mind":
                user_feat.append(dic['price'][price])
                creteria_to_take.append('price')
                ls.append('(casing.price+mb.price+gpu.price+ram.price+ssd.price+psu.price+cpu.price)')

            if brand!="Don't mind":
                user_feat.append(dic['brand'][brand])
                creteria_to_take.append('brand')
                ls.append('cpu.brand')

            for rs in ls_reason:
                if rs in reason:
                    user_feat.append(1)
                else:
                    user_feat.append(0)

            creteria_to_take.append('reason')
            ls.append('pcpackage.reason')

            if color !="Don't mind":
                user_feat.append(dic['color'][color])
                creteria_to_take.append('color')
                ls.append('pcpackage.color')


            for pr in ls_perf:
                if pr in perfomance:
                    user_feat.append(1)
                else:
                    user_feat.append(0)

            creteria_to_take.append('performance')
            ls.append('pcpackage.performance')




            result = db.engine.execute("SELECT pcpackage.id, "+', '.join(ls)+ " FROM pcpackage JOIN casing ON (pcpackage.casing=casing.id) JOIN mb ON (pcpackage.mb=mb.id) JOIN gpu ON (pcpackage.gpu = gpu.id) JOIN ram ON (pcpackage.ram=ram.id) JOIN ssd ON (pcpackage.ssd=ssd.id) JOIN psu ON (pcpackage.psu=psu.id) JOIN cpu ON (pcpackage.cpu=cpu.id) ORDER BY id DESC")
            #result = db.engine.execute("SELECT * FROM pcpackage;")


            sim = {}

            for row in result:
                i = 1

                feat = []
                if 'price' in creteria_to_take:
                    if row[i]<3000:
                        feat.append(0)
                    elif row[i]<5000:
                        feat.append(1)
                    else:
                        feat.append(2)
                    i+=1

                if 'brand' in creteria_to_take:

                    feat.append(dic['brand'][row[i]])

                    i+=1
                reasons_db = row[i].split(',')
                for rs in ls_reason:
                    if rs in reasons_db:
                        feat.append(1)
                    else:
                        feat.append(0)

                i+=1

                if 'color' in creteria_to_take:

                    feat.append(dic['color'][row[i]])
                    i+=1


                perf_db = row[i].split(',')

                for pr in ls_perf:
                    if pr in perf_db:
                        feat.append(1)
                    else:
                        feat.append(0)

                #consine similiarity to make comparison
                sim[row[0]] = int((1 - dist.pairwise([user_feat],[feat])[0][0])*100)




            sm = [(k,v) for k,v in sorted(sim.items(), key=lambda item: item[1],reverse=True)][0]
            print(sm)
            result = db.engine.execute("SELECT pcpackage.id,casing.name,mb.name,gpu.name,ram.name,ssd.name,psu.name,cpu.name,(casing.price+mb.price+gpu.price+ram.price+ssd.price+psu.price+cpu.price) FROM pcpackage JOIN casing ON (pcpackage.casing=casing.id) JOIN mb ON (pcpackage.mb=mb.id) JOIN gpu ON (pcpackage.gpu = gpu.id) JOIN ram ON (pcpackage.ram=ram.id) JOIN ssd ON (pcpackage.ssd=ssd.id) JOIN psu ON (pcpackage.psu=psu.id) JOIN cpu ON (pcpackage.cpu=cpu.id) WHERE pcpackage.id="+str(sm[0]))

            for row in result:
                rs = row

            rs = list(rs)
            rs.append(sm[1])


            parm = {'casing':rs[1].replace('/', ' '),
                    'mb':rs[2].replace('/', ' '),
                    'gpu':rs[3].replace('/', ' '),
                    'ram':rs[4].replace('/', ' '),
                    'ssd':rs[5].replace('/', ' '),
                    'psu':rs[6].replace('/', ' '),
                    'cpu':rs[7].replace('/', ' '),
                    'price':rs[8],
                    'similarity':rs[9]} 
            
           
            db.session.add(Facts(
            custID=request.form['id'], pricerange=request.form['price'], brandprefer=request.form['brand'],reason=reasontodb,color=request.form['color'],performance=performancetodb))
            db.session.commit()
            return redirect(url_for('recommendation',**parm))
        except:
            render_template('question.html')
    else:
        return render_template('question.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        custEmail = request.form['custEmail']
        custPass = request.form['custPass']
        customer = Customer.query.filter_by(custEmail=custEmail).first()
        if customer:
            if customer.custPass == custPass:
                login_user(customer)
                return redirect(url_for('home'))
        else:

            return "invalid email or password"
    return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(Customer(custName=request.form['custName'], custEmail=request.form['custEmail'],
                           custPhoneNo=request.form['custPhoneNo'], custAdd=request.form['custAdd'], custPass=request.form['custPass']))

            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/about')
def about():
    return render_template('about.html', message="WELCOME TO PALAMTECH PC BUILDER")


@app.route('/aboutbeforelogin')
def aboutbeforelogin():
    return render_template('aboutbeforelogin.html')


@app.route('/contact')
def contact():
    return render_template('contact.html', message="WELCOME TO PALAMTECH PC BUILDER")


@app.route('/writefeedback', methods=['POST', 'GET'])
def writefeedback():

    if request.method == 'POST':
        db.session.add(Feedbacks(custEmail=request.form['custEmail'], fbType=request.form['fbType'],
                       fbDate=request.form['fbDate'], fbDesc=request.form['fbDesc']))
        db.session.commit()
        return redirect(url_for('myfeedback'))
    else:
        return render_template('writefeedback.html')


@app.route('/myfeedback')
def myfeedback():
    custEmail = current_user.custEmail
    result = db.engine.execute(
        "SELECT * FROM feedbacks WHERE custEmail = %s", custEmail)
    return render_template("myfeedback.html", feedbacks=result)


@app.route('/contactbeforelogin')
def contactbeforelogin():
    return render_template("contactbeforelogin.html")


@app.route('/insert')
def insert():
    if request.method == 'POST':

        custName = request.form['custName']
        custEmail = request.form['custEmail']
        custPhoneNo = request.form['custPhoneNo']
        custAdd = request.form['custAdd']
        custPass = request.form['custPass']

        my_data = Customer(custName, custEmail, custPhoneNo, custAdd, custPass)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/productself1')
def productself1():
    return render_template('productself1.html')

@app.route('/updatefeedback/<int:fbID>', methods=['GET', 'POST'])
def updatefeedback(fbID):

    all_data = Feedbacks.query.all()
    feedback_to_update = Feedbacks.query.filter_by(fbID=fbID).first()
    if request.method == 'POST':

        feedback_to_update.custEmail = request.form['custEmail']
        feedback_to_update.fbType = request.form['fbType']
        feedback_to_update.fbDate = request.form['fbDate']
        feedback_to_update.fbDesc = request.form['fbDesc']
        feedback_to_update.feedback = Feedbacks(
            custEmail=feedback_to_update.custEmail, fbType=feedback_to_update.fbType, fbDate=feedback_to_update.fbDate, fbDesc=feedback_to_update.fbDesc)

        db.session.commit()
        return redirect('/myfeedback')

    return render_template('updatefeedback.html', feedback_to_update=feedback_to_update, feedback=all_data)

