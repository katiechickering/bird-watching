from flask_app import app
from flask_app.models import user
from flask import render_template, redirect, request, session

# Index route
@app.route('/')
def index():
    return redirect('/user/login')

# Login page
@app.route('/user/login')
def login():
    return render_template('index.html')

# Register a user
@app.post('/user/register/process')
def register_success():
    session['fname'] = request.form['fname']
    session['lname'] = request.form['lname']
    session['r_email'] = request.form['email']
    if not user.User.validate_reg(request.form):
        return redirect('/user/login')
    session.pop('fname', None)
    session.pop('lname', None)
    session.pop('r_email', None)
    id = user.User.create(request.form)
    session['id'] = id
    return redirect('/user/dashboard')

# Login a user
@app.post('/user/login/process')
def login_success():
    session['l_email'] = request.form['email']
    user_data = user.User.validate_login(request.form)
    if not user_data:
        return redirect('/user/login')
    session.pop('l_email', None)
    session['id'] = user_data.id
    return redirect('/user/dashboard')

# Logout a user
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/user/login')