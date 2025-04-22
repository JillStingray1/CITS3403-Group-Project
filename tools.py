from re import search
from models.Models import User
from flask import session

def validate_password(password: str) -> bool:
    """
    Checks if a inputted username is valid. Passwords should only contain all
    alphanumeric characters, and special characters !#+:=.?
    Args:
        password (string): the password sent to the srever

    Returns:
        boolean: describes whether the password fits the requirements and is safe to use in queries
    """
    if len(password) < 5 or len(password) > 35:
        return False
    san_password = search("[A-Za-z0-9!#+:=.?]+", password)
    if san_password:
        return san_password.group() == password
    return False


def validate_username(username: str) -> bool:
    """
    Checks if a inputted username is valid. Username should only contain
    alphanumeric characters (excluding decimals) and underscores, and must be
    at least 3 characters long.

    Args:
        username (string): the username set to the server

    Returns:
        boolean: describes whether the username fits the requirements and is safe to use in queries
    """
    if len(username) < 3 or len(username) > 25:
        return False
    san_username = search("[A-Za-z0-9_]+", username)
    if san_username:
        return san_username.group() == username
    return False

def save_login_session(user: User):
    """
    Saves the user login session state (different to ORM session).
    Args:
        user (User): The user object to save the session for.
    """
    session['user_id'] = user.id
    session['username'] = user.username
    session['logged_in'] = True
    return

def clear_login_session():
    """
    Clears the user login session state.
    """
    if 'user_id' not in session:
        return
    
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('logged_in', None)
    
    return