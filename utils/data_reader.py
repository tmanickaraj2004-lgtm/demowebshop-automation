"""Readers for external test data: CSV, Excel and SQLite, with validation."""
import csv
import re
import sqlite3
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "testdata"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(value):
    return bool(EMAIL_RE.match(value or ""))


def read_csv(filename):
    """Return a list of dict rows from testdata/<filename>."""
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def read_excel(filename, sheet=None):
    """Return a list of dict rows (first row = header) from testdata/<filename>."""
    wb = load_workbook(DATA_DIR / filename, data_only=True)
    ws = wb[sheet] if sheet else wb.active
    rows = list(ws.iter_rows(values_only=True))
    header = [str(h).strip() for h in rows[0]]
    return [
        {header[i]: ("" if v is None else str(v).strip()) for i, v in enumerate(r)}
        for r in rows[1:]
        if any(c is not None for c in r)
    ]


def read_db(query, db_name="test_users.db"):
    """Run a SELECT against the SQLite test database (seeded by db_helper)."""
    from utils.db_helper import seed_db

    seed_db(db_name)
    con = sqlite3.connect(DATA_DIR / db_name)
    con.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in con.execute(query).fetchall()]
    finally:
        con.close()


def validate_rows(rows, required):
    """Data validation: every required column must be non-empty (except those allowed blank)."""
    bad = [r for r in rows if any(r.get(c, "") == "" for c in required)]
    if bad:
        raise ValueError(f"Invalid test data rows (missing {required}): {bad}")
    return rows


def to_params(rows, *columns):
    """Convert dict rows to tuples for pytest.mark.parametrize."""
    return [tuple(r[c] for c in columns) for r in rows]
