"""Module 2 - Projects 4/5: the same core flows must behave identically in every browser.

Run with:  pytest tests/module2_crossbrowser --browser=chrome
           pytest tests/module2_crossbrowser --browser=firefox
"""
import pytest

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.search_page import SearchPage


@pytest.mark.smoke
def test_home_page_title_and_url(driver):
    assert "Demo Web Shop" in driver.title
    assert driver.current_url.startswith("https://demowebshop.tricentis.com")


def test_registration_and_logout(driver, new_user):
    page = RegisterPage(driver).register(
        new_user["first"], new_user["last"], new_user["email"], new_user["password"]
    )
    assert "Your registration completed" in page.success_message()
    page.logout()
    assert page.is_displayed(page.LOGIN_LINK)


def test_login_error_message_is_consistent(driver):
    page = LoginPage(driver).login("nobody_registered@mailtest.com", "Test@1234")
    assert "Login was unsuccessful" in page.error_text()


def test_search_works(driver):
    assert SearchPage(driver).search("computer").result_count() > 0


def test_add_to_cart(driver):
    cart = CartPage(driver).add_product("/computing-and-internet")
    assert cart.cart_count() == 1


def test_back_forward_navigation(driver):
    page = BasePage(driver)
    page.open("/login")
    page.open("/register")
    driver.back()
    assert driver.current_url.endswith("/login")
    driver.forward()
    assert driver.current_url.endswith("/register")


def test_cookies_are_set_and_cleared(driver):
    assert len(driver.get_cookies()) > 0
    driver.delete_all_cookies()
    assert driver.get_cookies() == []


def test_new_window_handles(driver):
    original = driver.current_window_handle
    driver.switch_to.new_window("tab")
    driver.get(BasePage.BASE_URL + "/login")
    assert len(driver.window_handles) == 2
    driver.close()
    driver.switch_to.window(original)
    assert len(driver.window_handles) == 1
