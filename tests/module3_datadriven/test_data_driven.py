"""Module 3 - Projects 7/8/9: data-driven tests fed from CSV, Excel and SQLite.

Demonstrates data parameterization (pytest.mark.parametrize), data validation
(validate_rows / is_valid_email) and data manipulation (unique emails, result write-back).
"""
import time

import pytest

from conftest import unique_email
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.search_page import SearchPage
from utils.data_reader import (is_valid_email, read_csv, read_db, read_excel,
                               to_params, validate_rows)

pytestmark = pytest.mark.data_driven

# ---- load + validate data at collection time ----
LOGIN_ROWS = validate_rows(read_csv("login_data.csv"), ["case_id", "password", "expected_result"])
REG_ROWS = validate_rows(read_excel("users.xlsx"), ["first", "last", "email_prefix", "password", "expected"])
SEARCH_ROWS = read_db("SELECT term, min_results FROM search_terms")


# ---------------- CSV: login ----------------
@pytest.mark.negative
@pytest.mark.parametrize(
    "email,password,expected",
    to_params(LOGIN_ROWS, "email", "password", "expected_result"),
    ids=[r["case_id"] for r in LOGIN_ROWS],
)
def test_login_from_csv(driver, email, password, expected):
    page = LoginPage(driver).login(email, password)
    text = page.error_text()
    # "a|b" in the CSV means: either message is acceptable
    assert any(option in text for option in expected.split("|"))


# ---------------- Excel: registration ----------------
@pytest.mark.parametrize(
    "row", REG_ROWS, ids=[r["email_prefix"] for r in REG_ROWS]
)
def test_registration_from_excel(driver, row):
    # data manipulation: make each run's email unique
    email = unique_email(row["email_prefix"])
    assert is_valid_email(email)
    page = RegisterPage(driver).register(
        row["first"], row["last"], email, row["password"], row["confirm"]
    )
    if "completed" in row["expected"]:
        assert row["expected"] in page.success_message()
    else:
        assert row["expected"] in page.errors()


# ---------------- SQLite: search ----------------
@pytest.mark.parametrize(
    "term,min_results",
    [(r["term"], r["min_results"]) for r in SEARCH_ROWS],
)
def test_search_from_database(driver, term, min_results):
    page = SearchPage(driver).search(term)
    if min_results == 0:
        assert page.no_results_message_shown()
    else:
        assert page.result_count() >= min_results


# ---------------- Data validation of the data itself ----------------
def test_data_files_are_valid():
    assert len(LOGIN_ROWS) >= 3
    assert all(r["expected_result"] for r in LOGIN_ROWS)
    assert all(is_valid_email(unique_email(r["email_prefix"])) for r in REG_ROWS)
    assert {r["term"] for r in SEARCH_ROWS}


# ---------------- Data manipulation: write results back ----------------
def test_write_results_to_excel(tmp_path):
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.append(["case_id", "executed_at"])
    for r in LOGIN_ROWS:
        ws.append([r["case_id"], time.strftime("%Y-%m-%d %H:%M:%S")])
    out = tmp_path / "results.xlsx"
    wb.save(out)
    assert out.exists()