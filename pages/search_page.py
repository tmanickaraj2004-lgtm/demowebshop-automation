from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SearchPage(BasePage):
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-item .product-title a")
    RESULTS_AREA = (By.CSS_SELECTOR, ".search-results")

    def search(self, term):
        self.open()
        self.type(self.SEARCH_BOX, term)
        self.click(self.SEARCH_BUTTON)
        self.wait.until(EC.url_contains("/search"))  # wait for results page
        return self

    def result_count(self):
        return len(self.find_all(self.PRODUCT_ITEMS))

    def result_titles(self):
        return [e.text for e in self.find_all(self.PRODUCT_TITLES)]

    def no_results_message_shown(self):
        return "No products were found" in self.page_text()