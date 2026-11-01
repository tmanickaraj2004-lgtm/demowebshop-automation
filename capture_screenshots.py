"""Takes REAL screenshots of the Demo Web Shop for one account.

Example:
  python capture_screenshots.py --email you@gmail.com --password Test@1234 --products /computing-and-internet,/fiction --qty 2,1 --wish /blue-jeans
"""
import argparse
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.driver_factory import create_driver

p = argparse.ArgumentParser()
p.add_argument("--email", required=True)
p.add_argument("--password", required=True, help="at least 6 characters")
p.add_argument("--first", default="Student")
p.add_argument("--last", default="User")
p.add_argument("--products", default="/computing-and-internet", help="comma separated product paths")
p.add_argument("--qty", default="1", help="comma separated quantities")
p.add_argument("--wish", default="/blue-jeans", help="product path for wishlist")
p.add_argument("--browser", default="chrome")
args = p.parse_args()

out = Path("my_screenshots")
out.mkdir(exist_ok=True)
tag = args.email.split("@")[0]

WISH_BUTTON = (By.CSS_SELECTOR,
               "[id^='add-to-wishlist-button'], input.add-to-wishlist-button, "
               "input[value='Add to wishlist'], input[value='Add to Wishlist']")


def add_to_wishlist(driver, cart, path):
    """Open a product page and click its 'Add to wishlist' button. Returns True if it worked."""
    cart.open(path)
    try:
        btn = WebDriverWait(driver, 6).until(lambda d: next(iter(d.find_elements(*WISH_BUTTON)), None))
    except TimeoutException:
        buttons = [(e.get_attribute("id"), e.get_attribute("value"))
                   for e in driver.find_elements(By.CSS_SELECTOR, "input[type='button'], input[type='submit']")]
        print(f"No wishlist button on {path}. Buttons found: {buttons}")
        return False
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)
    cart.find(cart.BAR_NOTIFICATION)
    return True


driver = create_driver(args.browser)
driver.set_window_size(1400, 1000)
try:
    driver.get("https://demowebshop.tricentis.com")

    # log in; if the account does not exist yet, register it
    login = LoginPage(driver).login(args.email, args.password)
    if not login.is_displayed(login.LOGOUT_LINK, timeout=8):
        reg = RegisterPage(driver).register(args.first, args.last, args.email, args.password)
        if not reg.is_displayed(reg.LOGOUT_LINK, timeout=8):
            raise SystemExit("Login/registration failed: " + reg.errors())

    # start with an empty cart so quantities are exactly what you asked for
    cart = CartPage(driver)
    cart.load()
    while cart.item_count() > 0:
        cart.remove_first()

    # add products to the cart
    paths = [x.strip() for x in args.products.split(",")]
    qtys = [x.strip() for x in args.qty.split(",")]
    qtys += ["1"] * (len(paths) - len(qtys))
    for path, qty in zip(paths, qtys):
        cart.add_product(path, qty)

    # add one product to the wishlist (try the requested one first, then fall back)
    candidates = [args.wish, "/smartphone", "/141-inch-laptop", "/health-book", "/fiction"]
    for path in candidates:
        if add_to_wishlist(driver, cart, path):
            print("Added to wishlist:", path)
            break
    else:
        driver.save_screenshot(str(out / f"{tag}_debug.png"))
        raise SystemExit("Could not find an 'Add to wishlist' button on any product page.")

    cart.open("/wishlist")
    cart.find((By.CSS_SELECTOR, "tr.cart-item-row"))
    wish_file = out / f"{tag}_wishlist.png"
    driver.save_screenshot(str(wish_file))

    cart.load()
    cart.find(cart.UNIT_PRICE)
    cart_file = out / f"{tag}_cart.png"
    driver.save_screenshot(str(cart_file))

    # Ex 3 style photo: log out, then try a wrong password so the site shows its real error
    cart.logout()
    bad = LoginPage(driver).login(args.email, "Wrong#Pass999")
    bad.error_text()  # waits until the site's error message is visible
    login_file = out / f"{tag}_login_error.png"
    driver.save_screenshot(str(login_file))

    print("Saved:", cart_file, wish_file, login_file, sep="\n  ")
finally:
    driver.quit()