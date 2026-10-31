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
