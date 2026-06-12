import re
from exceptions import InvalidEmailError, UnderageError


EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.%+\-]+@[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,6}$"
)

MINIMUM_AGE = 18


class RegistrationService:
    

    def __init__(self, platform_name: str = "DefaultPlatform"):
        # Internal invariant — the service is useless without an identity.
        assert platform_name and platform_name.strip(), (
            "RegistrationService requires a non-empty platform_name."
        )
        self.platform_name = platform_name.strip()



    def register_user(self, email: str, age: int) -> bool:
       
        # Validate email first
        self._validate_email(email)

        # Validate age second
        self._validate_age(age)

        return True

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _validate_email(self, email: str) -> None:
        """Raise InvalidEmailError for null/empty/malformed addresses."""
        if email is None:
            raise InvalidEmailError("None", reason="email must not be null")

        if not email.strip():
            raise InvalidEmailError(email, reason="email must not be empty")

        if not EMAIL_REGEX.match(email):
            raise InvalidEmailError(
                email,
                reason="does not match required format (identifier@domain.tld)",
            )

    def _validate_age(self, age: int) -> None:
        """Raise UnderageError when the applicant is below the minimum age."""
        if age < MINIMUM_AGE:
            raise UnderageError(age)



if __name__ == "__main__":
    print("=" * 50)
    print("   User Registration Validation System")
    print("=" * 50)

    service = RegistrationService(platform_name="MyPlatform")

    email = input("\nEnter email address: ").strip()

    while True:
        age_input = input("Enter age: ").strip()
        if age_input.lstrip("-").isdigit():
            age = int(age_input)
            break
        print("  Please enter a valid whole number for age.")

    print()
    try:
        service.register_user(email, age)
        print(" PASSED — Registration successful!")
        print(f"   Email : {email}")
        print(f"   Age   : {age}")
    except InvalidEmailError as e:
        print(" FAILED — Invalid Email")
        print(f"   {e}")
    except UnderageError as e:
        print(" FAILED — Underage Applicant")
        print(f"   {e}")

    print("=" * 50)