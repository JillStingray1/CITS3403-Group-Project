# TODO : add middleware for user auth on all routes except login and signup. also add encryption for passwords and
import re


def validate_password(password: str) -> bool:
    """
    _summary_

    Args:
        password (string): the password sent to the srever

    Returns:
        boolean: describes whether the password fits the requirements and is safe to use in queries
    """
    return True


def validate_username(username: str) -> bool:
    """
    Checks if a inputted username is valid. Username should only contain
    alphanumeric characters (excluding decimals) and underscores.

    Args:
        username (string): the username set to the server

    Returns:
        boolean: describes whether the username fits the requirements and is safe to use in queries
    """
    if len(username) < 3:
        return False
    san_username = re.search("[A-Za-z0-9_]+", username)
    if san_username:
        return san_username.group() == username
    return False
