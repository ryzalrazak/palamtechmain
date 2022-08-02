from http.client import FORBIDDEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from app import app, db
from app.model import Admin, Ram, Gpu, Ssd, Psu, Cpu, Feedbacks, Casing, Customer, Mb, Pcpackage
import os
from sklearn.neighbors import DistanceMetric
dist = DistanceMetric.get_metric('hamming')


@app.route('/loginAdmin', methods=['GET', 'POST'])
def loginAdmin():
    if request.method == 'GET':
        return render_template('loginAdmin.html')
    else:
        c = request.form['adminEmail']
        p = request.form['adminPass']
        data = Admin.query.filter_by(adminEmail=c, adminPass=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('allcust'))
        else:
            return redirect(url_for('loginAdmin'))

@app.route('/allcust')
def allcust():
    all_data = Customer.query.all()
    return render_template("allcust.html", customer=all_data)



@app.route('/feedbacks')
def feedbacks():
    result = db.engine.execute(
        "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail)")

    return render_template("feedbacks.html", feedbacks=result)


@app.route('/complaints')
def complaints():
    result = db.engine.execute(
        "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail) WHERE fbType = 'Complain'")
    return render_template("complaints.html", complaints=result)


@app.route('/suggestions')
def suggestions():
    result = db.engine.execute(
        "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail) WHERE fbType = 'Suggestions'")
    return render_template("suggestions.html", suggestions=result)


@app.route('/reviews')
def reviews():
    result = db.engine.execute(
        "SELECT feedbacks.fbID,customer.custEmail,customer.custName,feedbacks.fbType,feedbacks.fbDate,feedbacks.fbDesc FROM feedbacks INNER JOIN customer ON (feedbacks.custEmail = customer.custEmail) WHERE fbType = 'Review'")
    return render_template("reviews.html", reviews=result)




@app.route('/addcasing', methods=['POST', 'GET'])
def addcasing():
    all_data = Casing.query.all()
    if request.method == 'POST':

        db.session.add(Casing(
            name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addcasing')

    else:
        return render_template('addcasing.html', casing=all_data)


@app.route('/addmb', methods=['POST', 'GET'])
def addmb():
    all_data = Mb.query.all()
    if request.method == 'POST':

        db.session.add(
            Mb(name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addmb')

    else:
        return render_template('addmb.html', mb=all_data)


@app.route('/addgpu', methods=['POST', 'GET'])
def addgpu():
    all_data = Gpu.query.all()
    if request.method == 'POST':

        db.session.add(Gpu(
            name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addgpu')

    else:
        return render_template('addgpu.html', gpu=all_data)


@app.route('/addram', methods=['POST', 'GET'])
def addram():
    all_data = Ram.query.all()
    if request.method == 'POST':

        db.session.add(Ram(
            name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addram')

    else:
        return render_template('addram.html', ram=all_data)


@app.route('/addssd', methods=['POST', 'GET'])
def addssd():
    all_data = Ssd.query.all()
    if request.method == 'POST':

        db.session.add(Ssd(
            name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addssd')

    else:
        return render_template('addssd.html', ssd=all_data)


@app.route('/addpsu', methods=['POST', 'GET'])
def addpsu():
    all_data = Psu.query.all()
    if request.method == 'POST':

        db.session.add(Psu(
            name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addpsu')

    else:
        return render_template('addpsu.html', psu=all_data)


@app.route('/addcpu', methods=['POST', 'GET'])
def addcpu():
    all_data = Cpu.query.all()
    if request.method == 'POST':

        db.session.add(Cpu(
            name=request.form['name'], brand=request.form['brand'], price=request.form['price']))
        db.session.commit()

        return redirect('/addcpu')

    else:
        return render_template('addcpu.html', cpu=all_data)


@app.route('/addpackage', methods=['POST', 'GET'])
def addpackage():
    rcasing = db.engine.execute("SELECT id, name FROM casing ORDER BY name")
    rmobo = db.engine.execute("SELECT id, name FROM mb ORDER BY name")
    rgpu = db.engine.execute("SELECT id, name FROM gpu ORDER BY name")
    rram = db.engine.execute("SELECT id, name FROM ram ORDER BY name")
    rstorage = db.engine.execute("SELECT id, name FROM ssd ORDER BY name")
    rpsu = db.engine.execute("SELECT id, name FROM psu ORDER BY name")
    rcpu = db.engine.execute("SELECT id, name FROM cpu ORDER BY name")
    result = db.engine.execute("SELECT pcpackage.id, casing.name, mb.name,gpu.name,ram.name,ssd.name,psu.name,cpu.name,(casing.price+mb.price+gpu.price+ram.price+ssd.price+psu.price+cpu.price),pcpackage.reason,pcpackage.color,pcpackage.performance FROM pcpackage JOIN casing ON (pcpackage.casing=casing.id) JOIN mb ON (pcpackage.mb=mb.id) JOIN gpu ON (pcpackage.gpu = gpu.id) JOIN ram ON (pcpackage.ram=ram.id) JOIN ssd ON (pcpackage.ssd=ssd.id) JOIN psu ON (pcpackage.psu=psu.id) JOIN cpu ON (pcpackage.cpu=cpu.id) ORDER BY id DESC")

    if request.method == 'POST':
        db.session.add(Pcpackage(casing=request.form['casing'], mb=request.form['mb'], gpu=request.form['gpu'],
                       ram=request.form['ram'], ssd=request.form['ssd'], psu=request.form['psu'], cpu=request.form['cpu'],reason=request.form['reason'],color=request.form['color'],performance=request.form['performance']))
        db.session.commit()
        return redirect('/addpackage')

    else:
        return render_template('addpackage.html', casing=rcasing, mobo=rmobo, gpu=rgpu, ram=rram, storage=rstorage, psu=rpsu, cpu=rcpu, package = result)

@app.route('/updatecasing/<int:id>', methods=['GET', 'POST'])
def updatecasing(id):
    component_to_update = Casing.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Casing(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addcasing')
    return render_template('updatecasing.html', component_to_update=component_to_update)


@app.route('/updatemb/<int:id>', methods=['GET', 'POST'])
def updatemb(id):
    component_to_update = Mb.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Mb(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addmb')
    return render_template('updatemb.html', component_to_update=component_to_update)


@app.route('/updategpu/<int:id>', methods=['GET', 'POST'])
def updategpu(id):
    component_to_update = Gpu.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Gpu(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addgpu')
    return render_template('updategpu.html', component_to_update=component_to_update)


@app.route('/updateram/<int:id>', methods=['GET', 'POST'])
def updateram(id):
    component_to_update = Ram.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Ram(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addram')
    return render_template('updateram.html', component_to_update=component_to_update)


@app.route('/updatessd/<int:id>', methods=['GET', 'POST'])
def updatessd(id):
    component_to_update = Ssd.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Ssd(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addssd')
    return render_template('updatessd.html', component_to_update=component_to_update)


@app.route('/updatepsu/<int:id>', methods=['GET', 'POST'])
def updatepsu(id):
    component_to_update = Psu.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Psu(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addpsu')
    return render_template('updatepsu.html', component_to_update=component_to_update)


@app.route('/updatecpu/<int:id>', methods=['GET', 'POST'])
def updatecpu(id):
    component_to_update = Cpu.query.filter_by(id=id).first()
    if request.method == 'POST':
        component_to_update.name = request.form['name']
        component_to_update.brand = request.form['brand']
        component_to_update.price = request.form['price']
        component_to_update.component = Cpu(
            name=component_to_update.name, brand=component_to_update.brand, price=component_to_update.price)
        db.session.commit()
        return redirect('/addcpu')
    return render_template('updatecpu.html', component_to_update=component_to_update)

@app.route('/updatepackage/<int:id>',methods = ['GET','POST'])
def updatepackage(id):
    #category = Category.query.filter_by(catID=catID).first()
    all_data = Pcpackage.query.all()
    component_to_update = Pcpackage.query.filter_by(id=id).first()
    rcasing = db.engine.execute("SELECT id, name FROM casing")
    rmb = db.engine.execute("SELECT id, name FROM mb")
    rgpu = db.engine.execute("SELECT id, name FROM gpu")
    rram = db.engine.execute("SELECT id, name FROM ram")
    rssd = db.engine.execute("SELECT id, name FROM ssd")
    rpsu = db.engine.execute("SELECT id, name FROM psu")
    rcpu = db.engine.execute("SELECT id, name FROM cpu")
    
    if request.method == 'POST':
        component_to_update.casing = request.form['casing']
        component_to_update.mb = request.form['mb']
        component_to_update.gpu = request.form['gpu']
        component_to_update.ram = request.form['ram']
        component_to_update.ssd = request.form['ssd']
        component_to_update.psu = request.form['psu']
        component_to_update.cpu = request.form['cpu']
        component_to_update.reason = request.form['reason']
        component_to_update.color = request.form['color']
        component_to_update.performance = request.form['performance']
        component_to_update.component = Pcpackage(casing =component_to_update.casing ,mb=component_to_update.mb, gpu=component_to_update.gpu, ram = component_to_update.ram, ssd = component_to_update.ssd, psu = component_to_update.psu, cpu = component_to_update.cpu, reason=component_to_update.reason,color = component_to_update.color,performance = component_to_update.performance)

        db.session.commit()
        return redirect('/addpackage')
    return render_template('updatepackage.html',component_to_update=component_to_update, package=all_data,casing=rcasing, mb=rmb, gpu=rgpu, ram=rram, ssd=rssd, psu=rpsu, cpu=rcpu)





@app.route('/deletepackage/<int:id>')
def deletepackage(id):
    component_to_delete = Pcpackage.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addpackage')
    except:
        return "There was a problem deleting the component"

@app.route('/deletecasing/<int:id>')
def deletecasing(id):
    component_to_delete = Casing.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addcasing')
    except:
        return "There was a problem deleting the component"


@app.route('/deletemb/<int:id>')
def deletemb(id):
    component_to_delete = Mb.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addmb')
    except:
        return "There was a problem deleting the component"


@app.route('/deletegpu/<int:id>')
def deletegpu(id):
    component_to_delete = Gpu.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addgpu')
    except:
        return "There was a problem deleting the component"


@app.route('/deleteram/<int:id>')
def deleteram(id):
    component_to_delete = Ram.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addram')
    except:
        return "There was a problem deleting the component"


@app.route('/deletessd/<int:id>')
def deletessd(id):
    component_to_delete = Ssd.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addssd')
    except:
        return "There was a problem deleting the component"


@app.route('/deletepsu/<int:id>')
def deletepsu(id):
    component_to_delete = Psu.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addpsu')
    except:
        return "There was a problem deleting the component"


@app.route('/deletecpu/<int:id>')
def deletecpu(id):
    component_to_delete = Cpu.query.get_or_404(id)

    try:
        db.session.delete(component_to_delete)
        db.session.commit()
        return redirect('/addcpu')
    except:
        return "There was a problem deleting the component"


@app.route('/deletefeedback/<int:fbID>')
def deletefeedback(fbID):
    feedback_to_delete = Feedbacks.query.get_or_404(fbID)

    try:
        db.session.delete(feedback_to_delete)
        db.session.commit()
        return redirect('/myfeedback')
    except:
        return "There was a problem deleting the component"


