import pytest
from exceptions import InvalidEmailError, UnderageError
from registration_service import RegistrationService



@pytest.fixture
def service():
    """Return a RegistrationService configured for the test platform."""
    return RegistrationService(platform_name="TestPlatform")



class TestSuccessfulRegistration:

    def test_valid_email_and_adult_age_returns_true(self, service):
        assert service.register_user("alice@example.com", 25) is True

    def test_minimum_age_boundary_passes(self, service):
        """Exactly 18 must be accepted."""
        assert service.register_user("bob@domain.org", 18) is True

    def test_subdomain_email_is_accepted(self, service):
        assert service.register_user("user@mail.domain.co.uk", 30) is True

    def test_email_with_plus_tag_is_accepted(self, service):
        assert service.register_user("user+tag@example.com", 22) is True

    def test_email_with_dots_and_underscores(self, service):
        assert service.register_user("first.last_name@my-domain.net", 40) is True


class TestInvalidEmail:

    def test_none_email_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError) as exc_info:
            service.register_user(None, 25)
        assert "null" in str(exc_info.value).lower()

    def test_empty_string_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError) as exc_info:
            service.register_user("", 25)
        assert "empty" in str(exc_info.value).lower()

    def test_whitespace_only_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError):
            service.register_user("   ", 25)

    def test_missing_at_symbol_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError) as exc_info:
            service.register_user("invalidemail.com", 25)
        assert "invalidemail.com" in str(exc_info.value)

    def test_missing_domain_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError):
            service.register_user("user@", 25)

    def test_missing_tld_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError):
            service.register_user("user@domain", 25)

    def test_double_at_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError):
            service.register_user("user@@domain.com", 25)

    def test_spaces_in_email_raises_invalid_email_error(self, service):
        with pytest.raises(InvalidEmailError):
            service.register_user("us er@domain.com", 25)

    def test_invalid_email_error_inherits_from_value_error(self, service):
        """InvalidEmailError must be a subclass of ValueError."""
        with pytest.raises(ValueError):
            service.register_user("bademail", 25)

    def test_error_message_contains_offending_email(self, service):
        bad = "not-an-email"
        with pytest.raises(InvalidEmailError) as exc_info:
            service.register_user(bad, 25)
        assert bad in str(exc_info.value)



class TestUnderageApplicant:

    def test_age_below_minimum_raises_underage_error(self, service):
        with pytest.raises(UnderageError) as exc_info:
            service.register_user("teen@example.com", 17)
        assert "17" in str(exc_info.value)

    def test_age_zero_raises_underage_error(self, service):
        with pytest.raises(UnderageError):
            service.register_user("newborn@example.com", 0)

    def test_negative_age_raises_underage_error(self, service):
        with pytest.raises(UnderageError):
            service.register_user("user@example.com", -5)

    def test_underage_error_inherits_from_exception(self, service):
        """UnderageError must be a subclass of Exception."""
        with pytest.raises(Exception):
            service.register_user("user@example.com", 16)

    def test_error_message_contains_actual_and_minimum_age(self, service):
        with pytest.raises(UnderageError) as exc_info:
            service.register_user("young@example.com", 15)
        message = str(exc_info.value)
        assert "15" in message
        assert "18" in message

    def test_underage_error_exposes_age_attribute(self, service):
        with pytest.raises(UnderageError) as exc_info:
            service.register_user("user@example.com", 14)
        assert exc_info.value.age == 14



class TestValidationOrder:

    def test_invalid_email_takes_priority_over_underage(self, service):
        """When both inputs are wrong, InvalidEmailError should surface first."""
        with pytest.raises(InvalidEmailError):
            service.register_user("bad-email", 10)



class TestServiceInvariant:

    def test_empty_platform_name_raises_assertion_error(self):
        with pytest.raises(AssertionError):
            RegistrationService(platform_name="")

    def test_whitespace_platform_name_raises_assertion_error(self):
        with pytest.raises(AssertionError):
            RegistrationService(platform_name="   ")

    def test_valid_platform_name_creates_service(self):
        svc = RegistrationService(platform_name="MyApp")
        assert svc.platform_name == "MyApp"