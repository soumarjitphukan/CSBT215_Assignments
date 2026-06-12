"""
Custom exceptions for the user registration validation module.

- InvalidEmailError: inherits from ValueError (checked-style, bad input value)
- UnderageError: inherits from Exception (runtime-style, business rule violation)
"""


class InvalidEmailError(ValueError):
    """Raised when an email address fails format validation."""

    def __init__(self, email: str, reason: str = "invalid format"):
        self.email = email
        self.reason = reason
        super().__init__(
            f"Email address '{email}' is invalid: {reason}."
        )


class UnderageError(Exception):
    """Raised when a user does not meet the minimum age requirement."""

    MINIMUM_AGE = 18

    def __init__(self, age: int):
        self.age = age
        super().__init__(
            f"Registration denied: applicant age {age} is below the minimum "
            f"required age of {self.MINIMUM_AGE}."
        )