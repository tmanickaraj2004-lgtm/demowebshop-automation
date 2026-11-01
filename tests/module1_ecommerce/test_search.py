"""Module 1 - Project 1/3: product search (positive + negative)."""
import pytest

from pages.search_page import SearchPage


@pytest.mark.smoke
def test_search_valid_term_returns_results(driver):
    page = SearchPage(driver).search("computer")
    assert page.result_count() > 0
    assert any("computer" in t.lower() for t in page.result_titles())


@pytest.mark.negative
def test_search_no_match(driver):
    page = SearchPage(driver).search("zzzxqy")
    assert page.no_results_message_shown()
    assert page.result_count() == 0


@pytest.mark.negative
def test_search_term_too_short_shows_warning(driver):
    page = SearchPage(driver).search("ab")
    assert "minimum length is 3" in page.page_text()


@pytest.mark.negative
def test_search_empty_term_shows_alert(driver):
    page = SearchPage(driver)
    page.open()
    page.click(page.SEARCH_BUTTON)
    assert "Please enter some search keyword" in page.accept_alert()