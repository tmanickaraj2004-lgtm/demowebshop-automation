from decimal import Decimal

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart"
    ADD_TO_CART = (By.CSS_SELECTOR, "input.add-to-cart-button, input[value='Add to cart']")
    BAR_NOTIFICATION = (By.CSS_SELECTOR, "#bar-notification .content")
    ROWS = (By.CSS_SELECTOR, "tr.cart-item-row")
    QTY_INPUT = (By.CSS_SELECTOR, "input.qty-input")
    REMOVE_BOX = (By.CSS_SELECTOR, "input[name='removefromcart']")
    UPDATE_BUTTON = (By.NAME, "updatecart")
    UNIT_PRICE = (By.CSS_SELECTOR, "tr.cart-item-row .product-unit-price")
    LINE_TOTAL = (By.CSS_SELECTOR, "tr.cart-item-row .product-subtotal")
    SUBTOTAL = (By.CSS_SELECTOR, ".cart-total .product-price")
    TERMS = (By.ID, "termsofservice")
    CHECKOUT = (By.ID, "checkout")

    def add_product(self, product_path, qty=None):
        """Open a product page (e.g. '/computing-and-internet') and add it to the cart."""
        self.open(product_path)
        if qty is not None:
            self.type(self.QTY_INPUT, str(qty))
        self.click(self.ADD_TO_CART)
        self.find(self.BAR_NOTIFICATION)
        return self

    def load(self):
        return self.open(self.URL)

    @staticmethod
    def money(text):
        return Decimal(text.replace(",", "").strip())

    def item_count(self):
        return len(self.find_all(self.ROWS))

    def unit_price(self):
        return self.money(self.text_of(self.UNIT_PRICE))

    def line_total(self):
        return self.money(self.text_of(self.LINE_TOTAL))

    def subtotal(self):
        return self.money(self.text_of(self.SUBTOTAL))

    def set_quantity(self, qty):
        old = self.find(self.QTY_INPUT)
        self.type(self.QTY_INPUT, str(qty))
        self.click(self.UPDATE_BUTTON)
        self.wait.until(EC.staleness_of(old))  # page reloaded

    def remove_first(self):
        box = self.find(self.REMOVE_BOX)
        self.click(self.REMOVE_BOX)
        self.click(self.UPDATE_BUTTON)
        self.wait.until(EC.staleness_of(box))  # page reloaded

    def wait_for_page_text(self, text, timeout=10):
        try:
            self.wait.until(lambda d: text in self.page_text())
            return True
        except TimeoutException:
            return False

    def is_empty(self):
        return self.wait_for_page_text("Your Shopping Cart is empty")

    def accept_terms_and_checkout(self):
        self.click(self.TERMS)
        self.click(self.CHECKOUT)

    def checkout_without_terms(self):
        self.click(self.CHECKOUT)