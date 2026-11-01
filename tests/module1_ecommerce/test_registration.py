"""Module 1 - Project 1/3: user registration (positive + negative)."""
import pytest

from conftest import unique_email
from pages.register_page import RegisterPage


@pytest.mark.smoke
def test_register_valid_user(driver, new_user):
    page = RegisterPage(driver).register(
        new_user["first"], new_user["last"], new_user["email"], new_user["password"]
    )
    assert "Your registration completed" in page.success_message()
    assert page.logged_in_email() == new_user["email"]


@pytest.mark.negative
def test_register_existing_email(driver, new_user):
    RegisterPage(driver).register(
        new_user["first"], new_user["last"], new_user["email"], new_user["password"]
    )
    page = RegisterPage(driver)
    page.logout()
    page.register(new_user["first"], new_user["last"], new_user["email"], new_user["password"])
    assert "The specified email already exists" in page.errors()


@pytest.mark.negative
@pytest.mark.parametrize(
    "first,last,email,password,confirm,expected",
    [
        ("", "User", "ok@mailtest.com", "Test@1234", "Test@1234", "First name is required"),
        ("Test", "", "ok@mailtest.com", "Test@1234", "Test@1234", "Last name is required"),
        ("Test", "User", "", "Test@1234", "Test@1234", "Email is required"),
        ("Test", "User", "not-an-email", "Test@1234", "Test@1234", "Wrong email"),
        ("Test", "User", "ok@mailtest.com", "123", "123", "at least 6 characters"),
        ("Test", "User", "ok@mailtest.com", "Test@1234", "Different@1", "do not match"),
    ],
    ids=["no_first", "no_last", "no_email", "bad_email", "short_pw", "pw_mismatch"],
)
def test_register_validation_errors(driver, first, last, email, password, confirm, expected):
    page = RegisterPage(driver).register(first, last, email, password, confirm)
    assert expected in page.errors()
    assert not page.is_logged_in()