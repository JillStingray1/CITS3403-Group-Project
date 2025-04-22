from flask import Flask, session, request, jsonify, redirect, url_for
from app import app, db
from models.Models import User, Meeting, Timeslot
import bcrypt
from tools import validate_username, validate_password
from middleware.middleware import secure

# TODO: add authentication to the routes that require a user to be logged in. fill in the pass statements with the appropriate code. upon login, pass the user id to the session.

@app.route('/user', methods=['GET'])
#this route will be used to get the user details of the logged in user, useful for loading the users meetings
def get_user():
    pass

@app.route('/user/signup', methods=['POST'])
#this route will be used to create a new user. expects json as { username: 'username', password: 'password'}
def create_user():
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

        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['logged_in'] = True
        # setting the session variables to the current user
        
        return redirect(url_for('static', filename='main-menu.html')) # redirect to the main menu page after signup

@app.route('/user/login', methods=['POST'])
#this route will be used to login a user
def login_user():
    data = request.get_json()
    username = data.get('username')
    is_user = User.query.filter(User.username == username).first()
    if is_user is None:
        return jsonify({"error": "user not found"}), 400
    else: 
        password = data.get('password')
        if bcrypt.checkpw(password.encode('utf-8'), is_user.password_hash.encode('utf-8')):

            session['user_id'] = is_user.id
            session['username'] = is_user.username
            session['logged_in'] = True

            return redirect(url_for('static', filename='main-menu.html')) # redirect to the main menu page after successful login
        else:
            return jsonify({"error": "Invalid password"}), 400


@app.route('/user/logout', methods=['POST']) # auth required
@secure
#this route will be used to logout a user       
def logout_user():
    pass

