"""
Reusable validation helpers.
"""

import re


def is_valid_email(email: str) -> bool:
    """Check whether the provided string looks like a valid email address."""
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.

    Returns:
        Tuple of (is_valid, message).
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 128:
        return False, "Password must not exceed 128 characters."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    return True, "Password is valid."
