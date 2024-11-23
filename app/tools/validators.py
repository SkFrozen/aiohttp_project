import re


def is_valid_user_data(data: dict):
    """Check if the user data is valid."""
    email = bool(
        re.match(r"^[\w.%+-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$", data.get("emailInput"))
    )
    username = bool(re.match(r"^[\w]{4,50}$", data.get("usernameInput")))
    password = bool(
        re.match(
            r"^\S{6,100}$",
            data.get("passwordInput"),
        )
    )
    if not email:
        return "Email must contain @ and ."
    if not username:
        return "Username may contain a-Z, 0-9, _, min 4 char"
    if not password:
        return "Password must not contain spaces, min 6 char"
    return True
