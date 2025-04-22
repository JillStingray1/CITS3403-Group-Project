from flask import request, jsonify, redirect, url_for
from app import app, db
from models.Models import User
import bcrypt
from tools import validate_username, validate_password, save_login_session, clear_login_session
from middleware.middleware import secure

# TODO: add authentication to the routes that require a user to be logged in. fill in the pass statements with the appropriate code. upon login, pass the user id to the session.

@app.route('/user', methods=['GET'])
#this route will be used to get the user details of the logged in user, useful for loading the users meetings
def get_user():
    pass

@app.route('/user/signup', methods=['POST'])
def create_user():
    """
    Create a new user.
    Args:
        JSON { username: 'username', password: 'password'}

    Returns:
        On success, redurects to the main menu page and adds user to session.
        On failure, returns a JSON object with an error message.

    """
    data = request.get_json()
    username = data.get('username')
    is_username_valid = User.query.filter(User.username == username).first()
    if is_username_valid is not None: 
        return jsonify({"error": "Username already exists"}), 400
    else:
        password = data.get('password')
        if validate_username(username) is False:
            return jsonify({"error": "Invalid username"}), 400
        if validate_password(password) is False:
            return jsonify({"error": "Invalid password"}), 400
        
        new_user = User(username=username, password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))

        db.session.add(new_user)
        db.session.commit()

        save_login_session(new_user)
        # setting the session variables to the current user
        
        return redirect(url_for('static', filename='main-menu.html')) # redirect to the main menu page after signup

@app.route('/user/login', methods=['POST'])
def login_user():
    """
    login a user.

    Args:
        JSON { username: 'username', password: 'password'}

    Returns:
        On success, redurects to the main menu page adds user to session.
        On failure, returns a JSON object with an error message.
    """
    data = request.get_json()
    username = data.get('username')
    is_user = User.query.filter(User.username == username).first()
    if is_user is None:
        return jsonify({"error": "user not found"}), 400
    else: 
        password = data.get('password')
        if bcrypt.checkpw(password.encode('utf-8'), is_user.password_hash.encode('utf-8')):
        
            save_login_session(is_user)

            return redirect(url_for('static', filename='main-menu.html')) # redirect to the main menu page after successful login
        else:
            return jsonify({"error": "Invalid password"}), 400


@app.route('/user/logout', methods=['POST'])
@secure
#this route will be used to logout a user       
def logout_user():
    """
    Logout a user. Redirects to the index page."""
    clear_login_session()
    return redirect(url_for('static', filename='index.html'))
   

