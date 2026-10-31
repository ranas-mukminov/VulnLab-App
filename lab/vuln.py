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


from urllib.parse import urlparse

# Simulated internal hosts. No real network request is ever made:
# fetch_url_vuln returns a canned string, which is enough to show
# that an unvalidated URL reaches an internal address in the lab.
INTERNAL_HOSTS = {"169.254.169.254", "metadata.google.internal", "localhost", "127.0.0.1"}


def fetch_url_vuln(url):
    """VULNERABLE (SSRF): any URL is accepted, including internal hosts."""
    host = urlparse(url).hostname or ""
    if host in INTERNAL_HOSTS or host.endswith(".internal"):
        return f"internal lab record for {host}"
    return f"fetched lab page from {url}"


def access_admin_vuln(role_claim):
    """VULNERABLE (broken authentication): a client-supplied role claim
    is trusted. Claiming 'admin' opens the admin panel."""
    if role_claim == "admin":
        return "admin panel lab content"
    return "denied"
