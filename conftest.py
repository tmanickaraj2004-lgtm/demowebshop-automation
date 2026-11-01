import base64
import time
from pathlib import Path

import pytest

from pages.base_page import BasePage
from pages.register_page import RegisterPage
from utils.driver_factory import create_driver

REPORTS = Path(__file__).parent / "reports"
SHOTS = REPORTS / "screenshots"


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="chrome | firefox | edge")
    parser.addoption("--headless", action="store_true", help="run browsers headless")
    parser.addoption("--grid-url", default=None, help="Selenium Grid / cloud hub URL")
    parser.addoption("--browser-version", default=None, help="browser version (Grid/cloud)")


def pytest_collection_modifyitems(items):
    """Tag every test with its module marker based on its folder."""
    for item in items:
        path = str(item.fspath)
        if "module1_ecommerce" in path:
            item.add_marker(pytest.mark.module1)
        elif "module2_crossbrowser" in path:
            item.add_marker(pytest.mark.module2)
        elif "module3_datadriven" in path:
            item.add_marker(pytest.mark.module3)


@pytest.fixture
def driver(request):
    cfg = request.config
    d = create_driver(
        browser=cfg.getoption("--browser"),
        headless=cfg.getoption("--headless"),
        grid_url=cfg.getoption("--grid-url"),
        version=cfg.getoption("--browser-version"),
    )
    d.implicitly_wait(0)
    d.get(BasePage.BASE_URL)
    request.node.driver = d
    yield d
    d.quit()


@pytest.fixture
def browser_name(request):
    return request.config.getoption("--browser")


def unique_email(prefix="user"):
    return f"{prefix}_{int(time.time() * 1000)}@mailtest.com"


@pytest.fixture
def new_user():
    """Credentials for a brand-new, unique account."""
    return {
        "first": "Test",
        "last": "User",
        "email": unique_email("qa"),
        "password": "Test@1234",
    }


@pytest.fixture
def logged_in(driver, new_user):
    """A browser session already registered and logged in as a fresh user."""
    page = RegisterPage(driver).register(
        new_user["first"], new_user["last"], new_user["email"], new_user["password"]
    )
    assert "Your registration completed" in page.success_message()
    return new_user


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot when a test fails and embed it in the HTML report."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    d = getattr(item, "driver", None)
    if d is None:
        return
    SHOTS.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in item.name)
    path = SHOTS / f"{safe}_{int(time.time())}.png"
    try:
        d.save_screenshot(str(path))
        from pytest_html import extras

        report.extras = getattr(report, "extras", []) + [
            extras.image(base64.b64encode(path.read_bytes()).decode())
        ]
    except Exception:
        pass
