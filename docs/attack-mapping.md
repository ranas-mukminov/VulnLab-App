# MITRE ATT&CK mapping — VulnLab-App (illustrative, lab only)

This mapping is an exercise aid for the local lab cases. It is not
a formal ATT&CK assessment and makes no claim about any real system.

| Case | Mapping (illustrative) | Detection idea |
|------|------------------------|----------------|
| SQL injection | T1190 Exploit Public-Facing Application (Initial Access) | Web logs with SQL syntax in a query parameter |
| Reflected XSS | T1189 Drive-by Compromise (Initial Access) | Web logs with script tags in a query parameter |
| IDOR | T1078 Valid Accounts (Persistence / Privilege Escalation tactic family) — a valid session used to read another user's object | Access logs where caller and owner differ |
| SSRF | T1190 Exploit Public-Facing Application; outbound request to an internal host | Outbound / proxy logs to metadata or localhost addresses |
| Broken authentication | T1078 Valid Accounts — a claimed role accepted without an issued session | Admin-panel access without a valid issued session |

See `detections/sigma-rules.yml` for Sigma-style rules in lab
log format. They are detection format examples only; no live
telemetry claim is made for them.
