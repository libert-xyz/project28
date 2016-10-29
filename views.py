from flask import render_template, url_for, request, redirect,flash
from app import app,db
from models import User, Participante
from forms import AddUser, EditUser, LoginAdmin, ContestForm
from flask_login import login_required,logout_user,login_user,current_user
import os
import httplib2
import json
from flask import session as login_session

@app.route('/')
def index():
    return render_template('index.html')

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
            return redirect(url_for('judge'))
        else:
            return 'Invalid User or Password'
    return render_template('login.html',form=form)


@app.route('/judge')
@login_required
def judge():
    participantes = Participante.query.all()
    users = User.query.all()
    picture = login_session['picture']
    return render_template('admin.html',users=users)

    #return render_template('judge.html',participantes=participantes,picture=picture)

@app.route('/vote/<int:id>')
def vote(id):
    participante = Participante.query.filter_by(id=id).one()
    participante.votes = participante.votes +  4
    db.session.add(participante)
    db.session.commit()
    return 'ok'



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
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    login_session['access_token'] = access_token

    #Get User Picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    picture_result = h.request(url,'GET')[1]
    data_picture = json.loads(picture_result.decode())
    login_session['picture'] = data_picture['data']['url']


    # participante = Participante(name=data['name'],email=data['email'])
    #
    # db.session.add(participante)
    # db.session.commit()

    print ('Facebook info: %s' %fb_info)

    #return redirect(url_for('participantes',data=data))

    return participantes(data)

#@app.route('/participantes/<data>')
def participantes(data):
    # participantes = Participante.query.all()
    # return render_template('participante.html',participantes=participantes)


    print (data)
    try:
        Participante.query.filter_by(email=data['email']).one()
        return redirect(url_for('contest'))


    except:
        participante = Participante(name=data['name'],email=data['email'])
        #login_session['email'] = data['email']
        db.session.add(participante)
        db.session.commit()
        return redirect(url_for('contest'))

@app.route('/showParticipantes')
def showParticipantes():
    #login_session['email']

    participantes = Participante.query.all()
    return render_template('participante.html',participantes=participantes)

@app.route('/deleteParticipante/<int:id>',methods=['GET','POST'])
def deleteParticipante(id):
    p = Participante.query.filter_by(id=id).one()
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()

        flash('Participante Deleted')
        del login_session['username']
        del login_session['email']
        del login_session['facebook_id']
        del login_session['access_token']

        return redirect(url_for('showParticipantes'))

    return render_template('deleteparticipante.html',p=p)

#@app.route('/contest/<email>',methods=['GET','POST'])
@app.route('/contest',methods=['GET','POST'])
def contest():
    if 'email' in login_session:
        form = ContestForm(request.form)
        print ('LOGIN SESSION: %s' %login_session)
        participante = Participante.query.filter_by(email=login_session['email']).one()

        if participante.text == None:
            if request.method == 'POST':
                participante.text = form.text.data
                participante.phone = form.phone.data
                db.session.add(participante)
                db.session.commit()
                flash('Thank for participate')
                return render_template('incontest.html',participante=participante,picture=login_session['picture'])

            return render_template('contest.html',form=form,participante=participante,picture=login_session['picture'])
        else:
            return render_template('incontest.html',participante=participante,picture=login_session['picture'])

    else:
        return redirect(url_for('index'))
