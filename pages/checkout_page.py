from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    URL = "/onepagecheckout"

    BILLING_FIRST = (By.ID, "BillingNewAddress_FirstName")
    BILLING_COUNTRY = (By.ID, "BillingNewAddress_CountryId")
    BILLING_CITY = (By.ID, "BillingNewAddress_City")
    BILLING_ADDRESS = (By.ID, "BillingNewAddress_Address1")
    BILLING_ZIP = (By.ID, "BillingNewAddress_ZipPostalCode")
    BILLING_PHONE = (By.ID, "BillingNewAddress_PhoneNumber")

    BILLING_NEXT = (By.CSS_SELECTOR, "#billing-buttons-container input.button-1")
    SHIPPING_NEXT = (By.CSS_SELECTOR, "#shipping-buttons-container input.button-1")
    SHIPPING_METHOD_NEXT = (By.CSS_SELECTOR, "#shipping-method-buttons-container input.button-1")
    PAYMENT_METHOD_NEXT = (By.CSS_SELECTOR, "#payment-method-buttons-container input.button-1")
    PAYMENT_INFO_NEXT = (By.CSS_SELECTOR, "#payment-info-buttons-container input.button-1")
    CONFIRM = (By.CSS_SELECTOR, "#confirm-order-buttons-container input.button-1")

    SUCCESS_TITLE = (By.CSS_SELECTOR, ".order-completed .title strong")
    ORDER_NUMBER = (By.CSS_SELECTOR, ".order-completed ul.details li:first-child")
    BILLING_ERRORS = (By.CSS_SELECTOR, "#billing-new-address-form .field-validation-error")

    def fill_billing(self, country="India", city="Chennai", address="12 Anna Salai",
                     zip_code="600002", phone="9876543210"):
        """Fill the billing form if it is shown (new users); otherwise a saved address is used."""
        if self.is_displayed(self.BILLING_CITY, timeout=4):
            self.select_by_text(self.BILLING_COUNTRY, country)
            self.type(self.BILLING_CITY, city)
            self.type(self.BILLING_ADDRESS, address)
            self.type(self.BILLING_ZIP, zip_code)
            self.type(self.BILLING_PHONE, phone)

    def continue_billing(self):
        self.click(self.BILLING_NEXT)

    def complete_checkout(self, **billing):
        """Walk through every one-page-checkout step and place the order (Cash On Delivery)."""
        self.fill_billing(**billing)
        self.continue_billing()
        self.click(self.SHIPPING_NEXT)
        self.click(self.SHIPPING_METHOD_NEXT)
        self.click(self.PAYMENT_METHOD_NEXT)
        self.click(self.PAYMENT_INFO_NEXT)
        self.click(self.CONFIRM)
        return self

    def success_message(self):
        return self.text_of(self.SUCCESS_TITLE)

    def order_number(self):
        return self.text_of(self.ORDER_NUMBER).split(":")[-1].strip()

    def orders_page_text(self):
        self.open("/customer/orders")
        return self.page_text()
