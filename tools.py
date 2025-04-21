from re import search


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
