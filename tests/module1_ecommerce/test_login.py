"""Module 1 - Project 1/3: login (positive + negative)."""
import pytest

from pages.login_page import LoginPage
from pages.register_page import RegisterPage


@pytest.mark.smoke
def test_login_valid_credentials(driver, logged_in):
    RegisterPage(driver).logout()
    page = LoginPage(driver).login(logged_in["email"], logged_in["password"])
    assert page.is_logged_in()
    assert page.logged_in_email() == logged_in["email"]


@pytest.mark.negative
def test_login_wrong_password(driver, logged_in):
    RegisterPage(driver).logout()
    page = LoginPage(driver).login(logged_in["email"], "WrongPass@999")
    assert "credentials provided are incorrect" in page.error_text()
    assert not page.is_logged_in()


@pytest.mark.negative
def test_login_unregistered_email(driver):
    page = LoginPage(driver).login("nobody_registered@mailtest.com", "Test@1234")
    assert "Login was unsuccessful" in page.error_text()


@pytest.mark.negative
def test_login_empty_email(driver):
    page = LoginPage(driver).login("", "Test@1234")
    text = page.error_text()
    assert "Login was unsuccessful" in text or "Please enter your email" in text


@pytest.mark.negative
def test_login_invalid_email_format(driver):
    page = LoginPage(driver).login("invalid-email", "Test@1234")
    assert "Please enter a valid email address" in page.error_text()


@pytest.mark.smoke
def test_logout(driver, logged_in):
    page = RegisterPage(driver)
    page.logout()
    assert page.is_displayed(page.LOGIN_LINK)