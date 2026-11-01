from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    SUBMIT = (By.CSS_SELECTOR, "input.login-button")
    ERRORS = (By.CSS_SELECTOR, ".validation-summary-errors, .field-validation-error")

    def load(self):
        return self.open(self.URL)

    def login(self, email, password):
        self.load()
        self.type(self.EMAIL, email)
        if password:
            self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self

    def error_text(self):
        return self.wait_for_texts(self.ERRORS)