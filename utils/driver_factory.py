from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def create_driver(browser="chrome", headless=False, grid_url=None, version=None):
    """Create a local or remote (Selenium Grid / cloud) WebDriver.

    Selenium 4.6+ downloads the matching driver automatically (Selenium Manager).
    """
    browser = browser.lower()
    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
    else:
        browser = "chrome"
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    if version:
        options.browser_version = version  # used by Grid / BrowserStack / LambdaTest

    if grid_url:
        driver = webdriver.Remote(command_executor=grid_url, options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox(options=options)
    elif browser == "edge":
        driver = webdriver.Edge(options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_window_size(1920, 1080)
    return driver
