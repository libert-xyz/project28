from flask import render_template, url_for, request, redirect,flash
from app import app,db
from models import User
from forms import AddUser, EditUser, LoginAdmin
from flask_login import login_required,logout_user,login_user,current_user



@app.route('/')
def index():
    return 'Hello flask!'

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
