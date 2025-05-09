from re import search
from models.Models import User
from flask import session
from datetime import datetime, timedelta, date
from sqlalchemy import Date
import random
import string
from models.Meeting import Meeting


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
    session["user_id"] = user.id
    session["username"] = user.username
    session["logged_in"] = True
    session["meeting_id"] = None  # Initialize meeting_id to None or a default value
    return


def clear_login_session():
    """
    Clears the user login session state.
    """
    if "user_id" not in session:
        return

    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("logged_in", None)
    session.pop("meeting_id", None)  # Clear meeting_id from session

    return


def generate_share_code() -> str:
    """
    Generates a random share code for a meeting.
    The code is a 6-character alphanumeric string.
    Returns:
        str: The generated share code
    """
    characters = string.ascii_letters + string.digits
    share_code = "".join(random.choice(characters) for _ in range(16))

    return share_code


def get_best_time_from_slot(best_timeslot: int, start_date: datetime) -> datetime:
    """
    Converts the best time slot of a meeting into the datetime format

    Each timeslot represents a 15 minute increment in a 9-5 day, so each day has
    32 15 minute timeslots.

    Example: if a meeting has best timeslot 65, and starts on May 1st, the best
    time will start on May 3rd, at 9:15

    Args:
        `best_timeslot (int)`: The timeslot containing the most avaliable users
        for a meeting
        `start_date (datetime)`: best starting date for a meeing

    Returns:
        `datetime`: The best date and time for an even
    """
    best_days = best_timeslot // 32
    best_slot = best_timeslot % 32
    start_date.replace(hour=9, minute=0)
    best_time = start_date + timedelta(days=best_days, minutes=15 * best_slot)
    return best_time
