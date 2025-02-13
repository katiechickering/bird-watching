from flask_app import app
from flask_app.models import like
from flask import redirect, request

# Like a sighting
@app.post('/user/like/process')
def like_sighting():
    like.Like.like_sighting(request.form)
    return redirect(f'/user/sightings/{request.form['sighting_id']}')

# Unlike a sighting
@app.post('/user/unlike/process')
def unlike_sighting():
    print('process starting HIII')
    like.Like.unlike_sighting(request.form)
    return redirect(f'/user/sightings/{request.form['sighting_id']}')