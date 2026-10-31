"""Fixed implementations matching lab/vuln.py, flaw for flaw."""

import html
import sqlite3

from vuln import FICTIONAL_USERS, _db


def search_users_fixed(name):
    """FIXED: parameterised query — injection input matches nothing."""
    conn = _db()
    rows = conn.execute(
        "SELECT name, display FROM users WHERE name = ?", (name,)
    ).fetchall()
    conn.close()
    return rows


def render_greeting_fixed(name):
    """FIXED: user input escaped before rendering."""
    return f"<html><body><h1>Hello, {html.escape(name)}!</h1></body></html>"


def get_record_fixed(record_owner, caller):
    """FIXED: a caller may read only their own record."""
    if record_owner != caller:
        raise PermissionError("caller may read only their own record")
    records = {name: record for name, _, record in FICTIONAL_USERS}
    return records.get(record_owner)
