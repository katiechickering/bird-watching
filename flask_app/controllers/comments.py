from flask_app import app
from flask_app.models import comment, user
from flask_app.controllers import decorators
from flask import redirect, request, render_template, session

# Post a comment
@app.post('/user/comment/process')
def user_comment():
    if not comment.Comment.validate_comment(request.form):
        return redirect(f'/user/sightings/{request.form['sighting_id']}')
    comment.Comment.create_comment(request.form)
    return redirect(f'/user/sightings/{request.form['sighting_id']}')

# Delete a comment
@app.post('/user/delete_comment/process')
def delete_comment():
    comment.Comment.delete_comment(request.form)
    return redirect(f'/user/sightings/{request.form['sighting_id']}')

# Edit a comment page
@app.route('/user/edit/comment/<int:id>')
@decorators.login_required
def edit_comment_page(id):
    user_data = user.User.get_by_id(session['id'])
    comment_data = comment.Comment.get_by_id(id)
    if comment_data.user_id != user_data.id:
        return redirect(f'/user/sightings/{comment_data.sighting_id}')
    session['content'] = comment_data.content
    return render_template('edit_comment.html', user=user_data, comment=comment_data)

# Edit a comment
@app.post('/user/edit_comment/process')
def edit_comment():
    if not comment.Comment.validate_comment(request.form):
        return redirect(f'/user/edit/comment/{request.form['id']}')
    session.pop('content', None)
    comment.Comment.edit(request.form)
    return redirect(f'/user/sightings/{request.form['sighting_id']}')