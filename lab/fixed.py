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


from urllib.parse import urlparse

ALLOWED_FETCH_HOSTS = {"example.invalid"}
ISSUED_ADMIN_TOKENS = {"issued-lab-admin-token-7f3a"}


def fetch_url_fixed(url):
    """FIXED (SSRF): only allowlisted public lab hosts are fetched.
    Internal, localhost, and metadata hosts are rejected."""
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_FETCH_HOSTS:
        raise ValueError("host not on SSRF allowlist")
    return f"fetched lab page from {url}"


def access_admin_fixed(token):
    """FIXED (broken authentication): only a token that was actually
    issued opens the admin panel. A role claim alone is not enough."""
    if token in ISSUED_ADMIN_TOKENS:
        return "admin panel lab content"
    raise PermissionError("admin access requires an issued token")
