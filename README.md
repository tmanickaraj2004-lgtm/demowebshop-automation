# Demo Web Shop Automation (Python + Selenium + pytest)

Automation suite for https://demowebshop.tricentis.com, organised into the 3 modules of the course project list.

| Module | Projects | Folder | What it covers |
|---|---|---|---|
| 1 | 1, 2, 3 | `tests/module1_ecommerce` | Registration, login, search, cart, checkout, order processing. Positive + negative cases |
| 2 | 4, 5, 6 | `tests/module2_crossbrowser` | Same flows across Chrome/Firefox/Edge, UI elements, CSS, responsiveness, browser-specific checks |
| 3 | 7, 8, 9, 10 | `tests/module3_datadriven` + CI files | CSV / Excel / SQLite data-driven tests, parameterization, validation, git + GitHub Actions + Jenkins + reports |

## Setup
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python testdata/make_excel_data.py   # creates testdata/users.xlsx
```
Selenium 4.6+ downloads the browser drivers automatically. You only need the browsers installed.

## Run
```bash
pytest                                   # everything, Chrome
pytest -m module1                        # one module by marker
pytest tests/module2_crossbrowser --browser=firefox
pytest tests/module2_crossbrowser --browser=edge
pytest -m smoke --headless
pytest -n 4                              # parallel (pytest-xdist)
pytest --alluredir=reports/allure        # Allure results
```
Cross-browser versions: point at a Selenium Grid or BrowserStack/LambdaTest hub:
`pytest --browser=chrome --browser-version=120 --grid-url=http://localhost:4444/wd/hub`

HTML report: `reports/report.html`. Screenshots of failed tests are saved to `reports/screenshots/` and embedded in the report.

## Structure
```
pages/       Page Object Model (one class per page)
tests/       module1_ecommerce / module2_crossbrowser / module3_datadriven
testdata/    login_data.csv, users.xlsx (generated), SQLite DB (auto-seeded), css_baseline.json (auto-recorded)
utils/       driver_factory, data_reader (CSV/Excel/DB + validation), db_helper
conftest.py  fixtures, CLI options, failure screenshots
.github/workflows/tests.yml   CI matrix: 2 browsers x 3 modules
Jenkinsfile                   Jenkins alternative
```

## Version control (Project 10)
```bash
git init
git add .
git commit -m "Initial Selenium automation framework"
git branch -M main
git remote add origin https://github.com/<you>/demowebshop-automation.git
git push -u origin main
```
Every push triggers the GitHub Actions workflow; reports are uploaded as build artifacts.

## Notes
- The Demo Web Shop is a shared public practice site. Tests register unique throw-away users (`qa_<timestamp>@mailtest.com`), so no real accounts are used.
- The site is occasionally slow; if a test is flaky, raise the wait timeout in `pages/base_page.py`.
- First run of `test_css_matches_across_browsers` records `testdata/css_baseline.json` and skips; later runs on other browsers compare against it.
- Locators were written against the standard nopCommerce markup the site uses. I could not run the suite against the live site from my environment, so run it once locally and adjust any locator that differs.
