from re import search
from models import User
from flask import session
from datetime import datetime, timedelta, date
from sqlalchemy import Date
import random
import string
from models.Meeting import Meeting, Timeslot
from typing import List, Tuple


def validate_password(password: str) -> bool:
    """
    Checks if a inputted username is valid. Passwords should only contain all
    alphanumeric characters, and special characters !#+:=.?

    this function is used to test the regex used in form validators, should not be
    used elsewhere
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

    this function is used to test the regex used in form validators, should not be
    used elsewhere

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

def get_num_unavailable_per_timeslot(timeslots: list[Timeslot], meeting_length: int) -> dict[int, int]:
    """
    Calculates the unavaliability score of each timeslot in a meeting.

    The unavailability score is the sum of the total number of people unavailable
    on the timeslots for the duration of the meeting.

    The dictionary it returns has the key as the index of the timeslot, and
    the value as the score.

    Example:
        Take a 1 hour meeting
        At 15:00, 5 unavaliable
        At 15:15, 4 unavailable
        At 15:30, 3 unavailable
        at 15:45: 0 unavailable
        The unavalibility score of 15:00 will be 5 + 4 + 3 + 0 = 12


    Args:
        timeslots (list[Timeslot]): _description_
        meeting_length (int): _description_

    Returns:
        dict[int, int]: _description_
    """
    sorted_timeslots = sorted(timeslots, key=lambda x: x["order"])  # sort the timeslots by order
    amount_timeslots_needed = meeting_length // 15
    unavailable_scores = {}
    for i in range(len(sorted_timeslots)):
        current_slot = sorted_timeslots[i]
        total_unavailable = 0
        if i % 32 > (i + amount_timeslots_needed) % 32:
            break

        for j in range(amount_timeslots_needed):
            if (i + j) < len(sorted_timeslots):
                next_slot = sorted_timeslots[i + j]

                total_unavailable += len(next_slot["unavailable_users"])
            else:
                break

            # Save the total sum into dict_order
            unavailable_scores[current_slot["order"]] = total_unavailable
    return unavailable_scores
