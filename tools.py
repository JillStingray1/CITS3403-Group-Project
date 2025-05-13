from re import search
from models.Models import User
from flask import session
from datetime import datetime, timedelta, date
from sqlalchemy import Date
import random
import string
from models.Meeting import Meeting
from typing import List, Tuple


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


def get_best_time_from_slot(best_timeslot: int, start_date: date) -> datetime:
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
    if best_timeslot is None:
        best_timeslot = 0
    best_days = best_timeslot // 32
    best_slot = best_timeslot % 32
    best_time = datetime.combine(start_date, datetime.min.time())
    best_time = best_time.replace(hour=9, minute=0)
    print(best_time.strftime("%d %m %H:%M"))
    best_time += timedelta(days=best_days, minutes=15 * best_slot)
    return best_time


def format_meetings(
    meetings: list[Meeting],
) -> tuple[list[tuple[datetime, Meeting]], list[tuple[datetime, Meeting]]]:
    """
    Breaks a list of meetings into present and past meetings,
    and then sorts each in ascending order in terms of best times
    for current activities, and descending order in terms of past activities

    Args:
        meetings (list[Meeting]): A list of meetings that we would like to
        format

    Returns:
        tuple[list[tuple[datetime, Meeting]], list[tuple[datetime, Meeting]]]:
        A tuple with the first list containing current meetings, and the second
        list containing past meetings.

        Each list stores the meeting in a tuple in the form of
        (best_time, meeting)
    """
    current_activities = []
    past_activities = []
    current_date = date.today()
    for meeting in meetings:
        if meeting.end_date < current_date:  # type: ignore
            past_activities.append((get_best_time_from_slot(meeting.best_timeslot, meeting.start_date), meeting))  # type: ignore
        else:
            current_activities.append((get_best_time_from_slot(meeting.best_timeslot, meeting.start_date), meeting))  # type: ignore
    current_activities.sort(key=lambda item: item[0])
    past_activities.sort(key=lambda item: item[0], reverse=True)
    return (current_activities, past_activities)


def find_best_timeslot_windows(meeting: Meeting, window_size: int, top_k: int = 10
    ) -> List[Tuple[int, int]]:
    """
    Scans the meeting’s timeslots in order, summing unavailable_users over 
    each contiguous window of size `window_size`, and returns the top_k
    windows (order index, total_unavailable), sorted by fewest unavailable.
    """
    # pull out each slot’s order and its unavailable count
    slots = sorted(
        meeting.timeslots, 
        key=lambda ts: ts.order
    )
    orders = [ts.order for ts in slots]
    unavail_counts = [len(ts.unavailable_users) for ts in slots]

    scores = {}
    for i, base_order in enumerate(orders):
        running = 0
        for j in range(window_size):
            if i + j < len(unavail_counts):
                running += unavail_counts[i + j]
            else:
                break
        scores[base_order] = running

    # pick the top_k windows with smallest total_unavailable
    best = sorted(scores.items(), key=lambda kv: kv[1])[:top_k]
    return best