"""Module 1 - Project 1/3: cart, checkout and order processing (positive + negative)."""
from decimal import Decimal

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BOOK = "/computing-and-internet"  # simple product, no attributes required


@pytest.mark.smoke
def test_add_to_cart_updates_count_and_price(driver):
    cart = CartPage(driver).add_product(BOOK)
    assert cart.cart_count() == 1
    cart.load()
    assert cart.item_count() == 1
    assert cart.line_total() == cart.unit_price()  # qty 1
    assert cart.subtotal() == cart.line_total()


def test_update_quantity_recalculates_totals(driver):
    cart = CartPage(driver).add_product(BOOK)
    cart.load()
    unit = cart.unit_price()
    cart.set_quantity(3)
    assert cart.line_total() == unit * Decimal(3)
    assert cart.subtotal() == unit * Decimal(3)


def test_remove_item_empties_cart(driver):
    cart = CartPage(driver).add_product(BOOK)
    cart.load()
    cart.remove_first()
    assert cart.is_empty()


@pytest.mark.negative
def test_quantity_zero_removes_item(driver):
    cart = CartPage(driver).add_product(BOOK)
    cart.load()
    cart.set_quantity(0)
    assert cart.is_empty()


@pytest.mark.negative
def test_checkout_without_accepting_terms(driver):
    cart = CartPage(driver).add_product(BOOK)
    cart.load()
    cart.checkout_without_terms()
    assert cart.wait_for_page_text("accept the terms of service")
    assert "/onepagecheckout" not in driver.current_url


@pytest.mark.negative
def test_checkout_missing_billing_fields(driver, logged_in):
    cart = CartPage(driver).add_product(BOOK)
    cart.load()
    cart.accept_terms_and_checkout()
    checkout = CheckoutPage(driver)
    checkout.continue_billing()  # nothing filled in
    assert checkout.is_displayed(checkout.BILLING_ERRORS)


@pytest.mark.smoke
def test_full_checkout_places_order(driver, logged_in):
    cart = CartPage(driver).add_product(BOOK)
    cart.load()
    cart.accept_terms_and_checkout()
    checkout = CheckoutPage(driver).complete_checkout()
    assert "Your order has been successfully processed" in checkout.success_message()
    order_no = checkout.order_number()
    assert order_no.isdigit()
    # Order processing: the order must appear under My account -> Orders
    assert order_no in checkout.orders_page_text()
