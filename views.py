from flask import render_template, url_for, request, redirect,flash
from app import app,db
from models import User, Participante
from forms import AddUser, EditUser, LoginAdmin, ContestForm
from flask_login import login_required,logout_user,login_user,current_user
import os
import httplib2
import json


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
@login_required

def admin():
    users = User.query.all()
    return render_template('admin.html',users=users)

@app.route('/add', methods=['GET','POST'])
def add_users():
    form = AddUser(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data)
        user.email = (form.email.data)
        user.password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User Added')
        return redirect(url_for('admin'))

    return render_template('adduser.html',form=form)

@app.route('/user/edit/<int:id>',methods=['GET','POST'])

def edit_user(id):
    form = EditUser(request.form)
    user = User.query.filter_by(id=id).one()

    if request.method == 'POST':
        if form.email.data:
            user.email = form.email.data
        if form.name.data:
            user.name = form.name.data
        if form.password.data:
            user.password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('User Edited')
        return redirect(url_for('admin'))

    return render_template('edituser.html',form=form,user=user)



@app.route('/user/delete/<int:id>',methods=['GET','POST'])
def delete_user(id):
    user = User.query.filter_by(id=id).one()
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        flash('User Deleted')
        return redirect(url_for('admin'))

    return render_template('deleteuser.html',user=user)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginAdmin(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).one()
        print (form.email.data)
        if user.verify_password(form.password.data):
            login_user(user)
            flash('Welcome')
            return redirect(url_for('admin'))
        else:
            return 'Invalid User or Password'
    return render_template('login.html',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/fbconnect',methods=['POST'])
def fbconenct():
    access_token = request.data
    print ("Access token FB %s" %access_token.decode())
    #Exchange client token for long lived server-side

    app_id = os.environ['face_id']
    app_secret = os.environ['face_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
           app_id, app_secret, access_token.decode())

    h = httplib2.Http()
    result = h.request(url,'GET')[1]

    #Retrieve user info with the new token
    token = result.decode().split('&')[0]
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    fb_info = h.request(url, 'GET')[1]
    data = json.loads(fb_info.decode())

    # participante = Participante(name=data['name'],email=data['email'])
    #
    # db.session.add(participante)
    # db.session.commit()

    print ('Facebook info: %s' %fb_info)

    #return redirect(url_for('participantes',data=data))
    participantes(data)
    return 'ok'

#@app.route('/participantes/<data>')
def participantes(data):
    # participantes = Participante.query.all()
    # return render_template('participante.html',participantes=participantes)
    print (data)
    participante = Participante(name=data['name'],email=data['email'])

    db.session.add(participante)
    db.session.commit()
    return redirect(url_for('contest',id=participante.id))


@app.route('/showParticipantes')
def showParticipantes():
    participantes = Participante.query.all()
    return render_template('participante.html',participantes=participantes)

@app.route('/deleteParticipante/<int:id>',methods=['GET','POST'])
def deleteParticipante(id):
    p = Participante.query.filter_by(id=id).one()
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()
        flash('Participante Deleted')
        return redirect(url_for('showParticipantes'))

    return render_template('deleteparticipante.html',p=p)

@app.route('/contest/<int:id>',methods=['GET','POST'])
def contest(id):
    form = ContestForm(request.form)
    participante = Participante.query.filter_by(id=id).one()
    if request.method == 'POST':
        participante.text = form.text.data
        participante.phone = form.phone.data
        db.session.add(participante)
        db.session.commit()
        flash('Thank for this')
        return redirect(url_for('showParticipantes'))

    return render_template('contest.html',form=form,participante=participante)
