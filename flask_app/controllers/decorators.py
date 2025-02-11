from functools import wraps
from flask import session, redirect
from flask_app.models import user

def login_required(f):
    @wraps(f)
    def login_function(*args, **kwargs):
        if 'id' not in session:
            return redirect('/user/login')
        return f(*args, **kwargs)
    return login_function