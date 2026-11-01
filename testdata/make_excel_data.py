"""Generates testdata/users.xlsx (run once: python testdata/make_excel_data.py)."""
from pathlib import Path

from openpyxl import Workbook

rows = [
    ("first", "last", "email_prefix", "password", "confirm", "expected"),
    ("Arun", "Kumar", "arun.kumar", "Test@1234", "Test@1234", "Your registration completed"),
    ("Divya", "Raj", "divya.raj", "Secure#456", "Secure#456", "Your registration completed"),
    ("Meena", "S", "meena.s", "Pass@9876", "Pass@9876", "Your registration completed"),
    ("Ravi", "T", "ravi.t", "Test@1234", "Mismatch@1", "do not match"),
    ("Sana", "M", "sana.m", "123", "123", "at least 6 characters"),
]

wb = Workbook()
ws = wb.active
ws.title = "registration"
for r in rows:
    ws.append(r)
wb.save(Path(__file__).parent / "users.xlsx")
print("users.xlsx written")