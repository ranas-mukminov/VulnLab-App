# Security Policy

## This repository IS the vulnerability

VulnLab-App is intentionally vulnerable by design. That is the lab.
Do not file the lab flaws as security issues against this repository,
and do not "fix" the vulnerable version in place — the fixed version
already exists alongside it for comparison.

## Reporting a real problem

If you find a problem that is NOT one of the three documented lab
flaws — for example, the server binds to a non-localhost address, or
the lab writes outside its own directory — open an issue describing
the file and the behaviour. Do not include real credentials or data.

## Responsible use

Run locally only, on `127.0.0.1`, with fictional data only. Never
expose the lab to a network, never load real data into it, and never
use its techniques against a system you do not own. The exercises
are for learning detection and remediation, not for attacking real
systems.
