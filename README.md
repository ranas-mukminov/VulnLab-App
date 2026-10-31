# VulnLab-App

An intentionally vulnerable application for local training only.

> **WARNING — READ FIRST.** This application is deliberately insecure.
> Run it only on `127.0.0.1`, only on your own machine, only with the
> fictional data included here. Never expose it to a network, never put
> real user data or real credentials into it, and never deploy it
> anywhere. The whole point of the lab is that the flaws are visible
> and fixable in a safe place.

## What is in the lab

Three classic flaws, each shown twice: once vulnerable, once fixed.

| # | Flaw | Vulnerable code | Fixed code |
|---|---|---|---|
| 1 | SQL injection | `lab/vuln.py` — query built with string formatting | `lab/fixed.py` — parameterised query |
| 2 | Reflected cross-site scripting (XSS) | `lab/vuln.py` — user input rendered unescaped | `lab/fixed.py` — `html.escape` |
| 3 | Insecure direct object reference (IDOR) | `lab/vuln.py` — any record readable by any caller | `lab/fixed.py` — ownership check, `PermissionError` otherwise |

All data is fictional: users `lab-alice`, `lab-bob`, `lab-carol` with
placeholder records. No real person, no real account, no real secret.

## Run it locally

```bash
# Vulnerable version (localhost only, for study)
python3 lab/server.py --mode vuln --port 12700

# Fixed version (localhost only)
python3 lab/server.py --mode fixed --port 12701
```

The server binds to `127.0.0.1` only and refuses to bind to any other
address. Visit `http://127.0.0.1:12700/` and try the examples in
`docs/exercises.md`. Stop the server with Ctrl-C when you are done.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The tests prove, for each flaw, that the vulnerable version is
exploitable in the lab and that the fixed version is not — without
touching any real system.

## What this lab does not do

- It does not attack anything. The "attacker" and the "victim" are the
  same local process, with fictional data.
- It does not teach bypassing a real production safeguard. Every
  exercise ends with the fix, and the fix is the point.
- It does not contain real credentials, real user data, or any
  connection to a production database or service.

## Recent additions

- New cases: SSRF (simulated, no real network request) and broken authentication (role claim vs issued token), each with vulnerable and fixed versions, tests, and server routes (`/fetch`, `/admin`).
- `docs/attack-mapping.md` and `detections/sigma-rules.yml`: illustrative MITRE ATT&CK mapping and Sigma-style detection rules in lab log format.
