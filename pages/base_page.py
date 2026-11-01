from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    BASE_URL = "https://demowebshop.tricentis.com"

    # Header elements shared by every page
    LOGO = (By.CSS_SELECTOR, ".header-logo a img")
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "input.search-box-button")
    NAV_ITEMS = (By.CSS_SELECTOR, ".header-menu > ul.top-menu > li")
    LOGIN_LINK = (By.CLASS_NAME, "ico-login")
    REGISTER_LINK = (By.CLASS_NAME, "ico-register")
    LOGOUT_LINK = (By.CLASS_NAME, "ico-logout")
    ACCOUNT_LINK = (By.CSS_SELECTOR, ".header-links a.account")
    CART_LINK = (By.CLASS_NAME, "cart-label")
    CART_QTY = (By.CLASS_NAME, "cart-qty")

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---- navigation ----
    def open(self, path=""):
        self.driver.get(self.BASE_URL + path)
        return self

    # ---- element helpers ----
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text.strip()

    def is_displayed(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def select_by_text(self, locator, text):
        Select(self.find(locator)).select_by_visible_text(text)

    def page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def wait_for_texts(self, locator, timeout=10):
        """Wait until an element matching locator shows text, then return all texts."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: any(e.text.strip() for e in d.find_elements(*locator))
            )
        except TimeoutException:
            return ""
        return " | ".join(
            e.text.strip() for e in self.driver.find_elements(*locator) if e.text.strip()
        )

    def accept_alert(self, timeout=3):
        """Accept a JS alert and return its text ('' if none appeared)."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except (TimeoutException, NoAlertPresentException):
            return ""

    # ---- common header actions ----
    def go_to_login(self):
        self.click(self.LOGIN_LINK)

    def go_to_register(self):
        self.click(self.REGISTER_LINK)

    def logout(self):
        self.click(self.LOGOUT_LINK)

    def logged_in_email(self):
        return self.text_of(self.ACCOUNT_LINK)

    def is_logged_in(self):
        return self.is_displayed(self.LOGOUT_LINK)

    def cart_count(self):
        raw = self.text_of(self.CART_QTY)  # looks like "(2)"
        return int(raw.strip("()"))