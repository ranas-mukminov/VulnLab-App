> **Problem:** reading about SQL injection, XSS, IDOR, SSRF and broken authentication is not the same as seeing the vulnerable code next to the fixed code.
>
> **What this is:** an intentionally vulnerable local training app — each flaw shown twice, vulnerable and fixed, with tests.
>
> > **WARNING — LAB ONLY.** This app is deliberately insecure. Run it only on `127.0.0.1`, only on your own machine, only with the fictional data included here. Never expose it, never put real data or real credentials into it, never deploy it.
>
> **Who it is for:** learners and trainers who want a safe, local place to practise finding and fixing web flaws.
>
> **Quickstart:**
>
> ```bash
> git clone https://github.com/ranas-mukminov/VulnLab-App.git
> cd VulnLab-App
> python3 -m unittest discover -s tests -v
> python3 lab/server.py --mode vuln --port 12700
> ```
>
> Then visit `http://127.0.0.1:12700/` and try the exercises in `docs/exercises.md`. **Sample result (verified):** tests `14 OK`; the local server homepage lists the routes `/search`, `/greet`, `/record`, `/fetch`, `/admin`.
>
[![CI](https://github.com/ranas-mukminov/VulnLab-App/actions/workflows/tests.yml/badge.svg)](https://github.com/ranas-mukminov/VulnLab-App/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---
# VulnLab-App

An intentionally vulnerable application for local training only.

> **WARNING — READ FIRST.** This application is deliberately insecure.
> Run it only on `127.0.0.1`, only on your own machine, only with the
> fictional data included here. Never expose it to a network, never put
> real user data or real credentials into it, and never deploy it
> anywhere. The whole point of the lab is that the flaws are visible
> and fixable in a safe place.

## What is in the lab

Five flaws, each shown twice: once vulnerable, once fixed.

| # | Flaw | Vulnerable code | Fixed code |
|---|---|---|---|
| 1 | SQL injection | `lab/vuln.py` — query built with string formatting | `lab/fixed.py` — parameterised query |
| 2 | Reflected cross-site scripting (XSS) | `lab/vuln.py` — user input rendered unescaped | `lab/fixed.py` — `html.escape` |
| 3 | Insecure direct object reference (IDOR) | `lab/vuln.py` — any record readable by any caller | `lab/fixed.py` — ownership check, `PermissionError` otherwise |
| 4 | Server-side request forgery (SSRF, simulated) | `lab/vuln.py` — internal hosts fetched | `lab/fixed.py` — allowlist, internal/metadata hosts rejected |
| 5 | Broken authentication | `lab/vuln.py` — client-supplied role claim trusted | `lab/fixed.py` — issued token required |

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
