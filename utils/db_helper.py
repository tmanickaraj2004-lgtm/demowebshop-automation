"""SQLite helper: seeds a small test database used by the data-driven module."""
import sqlite3

from utils.data_reader import DATA_DIR

SEARCH_TERMS = [
    ("computer", 1, "valid"),
    ("laptop", 1, "valid"),
    ("jewelry", 1, "valid"),
    ("zzzxqy", 0, "no_match"),
]

USERS = [
    ("db_user_one", "Test@123"),
    ("db_user_two", "Secure#456"),
]


def seed_db(db_name="test_users.db"):
    con = sqlite3.connect(DATA_DIR / db_name)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS search_terms "
        "(term TEXT PRIMARY KEY, min_results INTEGER, kind TEXT)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (prefix TEXT PRIMARY KEY, password TEXT)"
    )
    cur.executemany("INSERT OR IGNORE INTO search_terms VALUES (?,?,?)", SEARCH_TERMS)
    cur.executemany("INSERT OR IGNORE INTO users VALUES (?,?)", USERS)
    con.commit()
    con.close()
