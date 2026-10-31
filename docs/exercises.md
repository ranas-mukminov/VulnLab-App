# Exercises (local lab only)

Run the vulnerable server on one port and the fixed server on another,
then compare. All inputs below are fictional lab inputs.

## 1. SQL injection

Vulnerable: `http://127.0.0.1:12700/search?name=' OR '1'='1`
returns every fictional user. Fixed, on the fixed port, the same input
returns no matches, because it is treated as a literal name.

Lesson: never build a query from user input. Parameterise it.

## 2. Reflected XSS

Vulnerable: `http://127.0.0.1:12700/greet?name=<script>alert(1)</script>`
renders the script tag unescaped. Fixed: the same input is rendered as
escaped text, so no script runs.

Lesson: escape user input at render time, every time, without exception.

## 3. IDOR

Vulnerable: `http://127.0.0.1:12700/record?owner=lab-bob&caller=lab-alice`
returns Bob's lab record to Alice. Fixed: the same request returns 403,
because a caller may read only their own record.

Lesson: authorisation is checked on the server, per object, per request
— never trust that a client will only ask for its own data.

## After each exercise

Write down, in one sentence each: what the flaw was, why the fix works,
and what test would catch a regression. That sentence is the deliverable
of the exercise, not the exploit.


## 4. SSRF (simulated, no real fetch)

Vulnerable: `http://127.0.0.1:12700/fetch?url=http://169.254.169.254/`
returns an internal lab record, because the URL is never validated.
Fixed: the same request returns 400, because only allowlisted hosts
are accepted. The lab never makes a real network request in either
mode — the vulnerable version returns a canned string, which is
enough to demonstrate the missing validation.

Lesson: validate and allowlist outbound URLs; never let user input
choose an internal address.

## 5. Broken authentication

Vulnerable: `http://127.0.0.1:12700/admin?role=admin` opens the
admin panel, because a client-supplied role claim is trusted.
Fixed: `http://127.0.0.1:12700/admin?token=issued-lab-admin-token-7f3a`
is required — a role claim alone returns 403.

Lesson: authorisation is decided server-side from an issued
session, never from a value the client asserts about itself.
