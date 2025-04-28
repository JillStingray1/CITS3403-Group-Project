# TODO : add middleware for user auth on all routes except login and signup. also add encryption for passwords and
from functools import wraps
from flask import request, session, redirect, url_for

def secure(f):
    """
    Middleware to check if a user is logged in.
    """
    @wraps(f)
    def check_login(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('static', filename='index.html'))
        return f(*args, **kwargs)
    return check_login