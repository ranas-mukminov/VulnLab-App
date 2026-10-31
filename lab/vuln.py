"""Intentionally vulnerable implementations — LAB ONLY, localhost only.

Do not copy these functions into a real application. Each one has a
matching fixed version in lab/fixed.py, and the difference between
them is the lesson of this lab.
"""

import sqlite3

FICTIONAL_USERS = [
    ("lab-alice", "Alice (lab)", "alice-lab-record"),
    ("lab-bob", "Bob (lab)", "bob-lab-record"),
    ("lab-carol", "Carol (lab)", "carol-lab-record"),
]


def _db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (name TEXT, display TEXT, record TEXT)")
    conn.executemany("INSERT INTO users VALUES (?, ?, ?)", FICTIONAL_USERS)
    return conn


def search_users_vuln(name):
    """VULNERABLE: SQL built with string formatting (SQL injection)."""
    conn = _db()
    query = f"SELECT name, display FROM users WHERE name = '{name}'"
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows


def render_greeting_vuln(name):
    """VULNERABLE: user input rendered without escaping (reflected XSS)."""
    return f"<html><body><h1>Hello, {name}!</h1></body></html>"


def get_record_vuln(record_owner, caller):
    """VULNERABLE: no ownership check (IDOR) — any caller reads any record."""
    records = {name: record for name, _, record in FICTIONAL_USERS}
    return records.get(record_owner)
