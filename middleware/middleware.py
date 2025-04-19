# TODO : add middleware for user auth on all routes except login and signup. also add encryption for passwords and


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
    _summary_

    Args:
        username (string): the username set to the server

    Returns:
        boolean: describes whether the username fits the requirements and is safe to use in queries
    """
    return username.isalnum()
