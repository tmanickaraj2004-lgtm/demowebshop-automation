"""Module 2 - Project 6: UI elements, CSS styling, responsiveness, browser-specific checks."""
import json
import re
from pathlib import Path

import pytest

from pages.base_page import BasePage

pytestmark = pytest.mark.ui

BASELINE = Path(__file__).resolve().parents[2] / "testdata" / "css_baseline.json"
SHOTS = Path(__file__).resolve().parents[2] / "reports" / "screenshots"

NAV_LABELS = ["BOOKS", "COMPUTERS", "ELECTRONICS", "APPAREL & SHOES",
              "DIGITAL DOWNLOADS", "JEWELRY", "GIFT CARDS"]


# ---------------- UI elements ----------------
def test_logo_is_displayed(driver):
    assert BasePage(driver).is_displayed(BasePage.LOGO)


def test_navigation_menu_items(driver):
    items = BasePage(driver).find_all(BasePage.NAV_ITEMS)
    labels = [i.text.strip().upper() for i in items]
    assert labels == NAV_LABELS


def test_search_box_and_button_enabled(driver):
    page = BasePage(driver)
    assert page.find(page.SEARCH_BOX).is_enabled()
    assert page.find(page.SEARCH_BUTTON).is_enabled()


def test_header_links_for_guest(driver):
    page = BasePage(driver)
    assert page.is_displayed(page.REGISTER_LINK)
    assert page.is_displayed(page.LOGIN_LINK)
    assert "Shopping cart" in page.text_of(page.CART_LINK)


# ---------------- CSS styling ----------------
def _norm(value):
    """Normalise colours: 'rgba(175, 3, 4, 1)' and 'rgb(175, 3, 4)' are the same colour."""
    m = re.fullmatch(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)", value.strip())
    if not m:
        return value
    r, g, b, a = m.groups()
    if a is not None and float(a) != 1:
        return f"rgba({r}, {g}, {b}, {a})"
    return f"rgb({r}, {g}, {b})"


def _css_snapshot(driver):
    page = BasePage(driver)
    nav = driver.find_element("css selector", ".header-menu")
    link = page.find(page.LOGIN_LINK)
    btn = page.find(page.SEARCH_BUTTON)
    body = driver.find_element("tag name", "body")
    return {
        "nav_background": nav.value_of_css_property("background-color"),
        "login_link_color": link.value_of_css_property("color"),
        "search_button_cursor": btn.value_of_css_property("cursor"),
        "body_font_size": body.value_of_css_property("font-size"),
    }


def test_css_matches_across_browsers(driver, browser_name):
    """First run stores a baseline; later runs (any browser) must match it."""
    snap = {k: _norm(v) for k, v in _css_snapshot(driver).items()}
    if not BASELINE.exists():
        BASELINE.write_text(json.dumps({"recorded_with": browser_name, **snap}, indent=2))
        pytest.skip("CSS baseline recorded; re-run to compare")
    expected = json.loads(BASELINE.read_text())
    expected.pop("recorded_with", None)
    expected = {k: _norm(v) for k, v in expected.items()}
    assert snap == expected


def test_nav_bar_has_dark_background(driver):
    bg = _css_snapshot(driver)["nav_background"]
    r, g, b = [int(x) for x in bg.replace("rgba(", "").replace("rgb(", "").rstrip(")").split(",")[:3]]
    assert max(r, g, b) < 100, f"nav background not dark: {bg}"


# ---------------- Responsiveness ----------------
@pytest.mark.parametrize(
    "name,width,height",
    [("mobile", 375, 812), ("tablet", 768, 1024), ("laptop", 1366, 768), ("desktop", 1920, 1080)],
)
def test_layout_at_viewport(driver, browser_name, name, width, height):
    driver.set_window_size(width, height)
    page = BasePage(driver)
    page.open()
    assert page.is_displayed(page.LOGO)
    assert page.is_displayed(page.SEARCH_BOX)
    SHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SHOTS / f"home_{browser_name}_{name}.png"))
    inner = driver.execute_script("return window.innerWidth")
    assert inner > 0


# ---------------- Browser-specific ----------------
def test_user_agent_matches_selected_browser(driver, browser_name):
    ua = driver.execute_script("return navigator.userAgent").lower()
    expected = {"chrome": "chrome", "firefox": "firefox", "edge": "edg"}[browser_name]
    assert expected in ua


def test_javascript_enabled_and_local_storage(driver):
    driver.execute_script("window.localStorage.setItem('qa','1')")
    assert driver.execute_script("return window.localStorage.getItem('qa')") == "1"