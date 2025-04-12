from flask import Flask, session
from app import app

# TODO: add authentication to the routes that require a user to be logged in. fill in the pass statements with the appropriate code. upon login, pass the user id to the session.

@app.route('/user', methods=['GET'])
#this route will be used to get the user details of the logged in user, useful for loading the users meetings
def get_user():
    pass

@app.route('/user', methods=['POST'])
#this route will be used to create a new user
def create_user():
    pass

@app.route('/user/login', methods=['POST'])
#this route will be used to login a user
def login_user():
    pass

@app.route('/user/logout', methods=['POST']) # auth required
#this route will be used to logout a user       
def logout_user():
    pass

