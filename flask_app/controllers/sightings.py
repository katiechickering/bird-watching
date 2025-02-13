from flask_app import app
from flask_app.models import sighting, user, like, comment
from flask import render_template, session, redirect, request
from flask_app.controllers import decorators

# Dashboard page
@app.route('/user/dashboard')
@decorators.login_required
def dashboard():
    user_data = user.User.get_by_id(session['id'])
    sightings = sighting.Sighting.get_all()
    return render_template('sightings.html', user=user_data, sightings=sightings)

# Post a sighting page
@app.route('/user/sightings/new')
@decorators.login_required
def new_sightings_page():
    user_data = user.User.get_by_id(session['id'])
    return render_template('new_sighting.html', user=user_data)

# Delete a sighting
@app.post('/user/delete/process/')
def delete():
    sighting.Sighting.delete_sighting(request.form)
    return redirect('/user/dashboard')

# Create a new sighting
@app.post('/user/sighting/process')
def create_sighting():
    if not sighting.Sighting.validate_sighting(request.form):
        session['n-species'] = request.form['species']
        session['n-location'] = request.form['location']
        session['n-datetime'] = request.form['datetime']
        session['n-number'] = request.form['number']
        session['n-description'] = request.form['description']
        return redirect('/user/sightings/new')
    sighting.Sighting.create_sighting(request.form)
    session.pop('n-species', None)
    session.pop('n-location', None)
    session.pop('n-datetime', None)
    session.pop('n-number', None)
    session.pop('n-description', None)
    return redirect('/user/dashboard')

# Edit a sighting page
@app.route('/user/sightings/edit/<int:id>')
@decorators.login_required
def edit_sighting_page(id):
    user_data = user.User.get_by_id(session['id'])
    sighting_data = sighting.Sighting.get_by_id(id)
    if sighting_data.user_id != user_data.id:
        return redirect('/user/dashboard')
    session['e-species'] = sighting_data.species
    session['e-location'] = sighting_data.location
    session['e-datetime'] = sighting_data.datetime
    session['e-number'] = sighting_data.number
    session['e-description'] = sighting_data.description
    return render_template('edit_sighting.html', sighting=sighting_data, user=user_data)

# Edit a sighting
@app.post('/user/edit/process')
def edit_sighting():
    if not sighting.Sighting.validate_sighting(request.form):
        return redirect(f'/user/sightings/edit/{request.form['id']}')
    session.pop('e-species', None)
    session.pop('e-location', None)
    session.pop('e-datetime', None)
    session.pop('e-number', None)
    session.pop('e-description', None)
    sighting.Sighting.edit(request.form)
    return redirect('/user/dashboard')

# Show a sighting page
@app.route('/user/sightings/<int:id>')
@decorators.login_required
def show_sighting_page(id):
    user_data = user.User.get_by_id(session['id'])
    sighting_data = sighting.Sighting.get_by_id(id)
    likes = like.Like.get_likes_from_sighting(id)
    comments = comment.Comment.get_all()
    return render_template('show_sighting.html', sighting=sighting_data, user=user_data, likes=likes, comments=comments)