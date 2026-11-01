from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    URL = "/register"
    GENDER_MALE = (By.ID, "gender-male")
    GENDER_FEMALE = (By.ID, "gender-female")
    FIRST_NAME = (By.ID, "FirstName")
    LAST_NAME = (By.ID, "LastName")
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    CONFIRM = (By.ID, "ConfirmPassword")
    SUBMIT = (By.ID, "register-button")
    RESULT = (By.CSS_SELECTOR, ".result")
    CONTINUE = (By.CSS_SELECTOR, "input.register-continue-button")
    ERRORS = (By.CSS_SELECTOR, ".validation-summary-errors, .field-validation-error")

    def load(self):
        return self.open(self.URL)

    def register(self, first, last, email, password, confirm=None, gender="male"):
        self.load()
        self.click(self.GENDER_MALE if gender == "male" else self.GENDER_FEMALE)
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.type(self.CONFIRM, password if confirm is None else confirm)
        self.click(self.SUBMIT)
        return self

    def success_message(self):
        return self.text_of(self.RESULT)

    def errors(self):
        """All validation error text visible on the page (field + summary)."""
        return self.wait_for_texts(self.ERRORS)