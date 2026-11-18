# Part 2 verification

## Commands

```bash
.semgrep-venv/bin/semgrep scan --config auto
.semgrep-venv/bin/semgrep scan --config semgrep-local/rules.yml
.venv/bin/pip-audit -r requirements.txt
.venv/bin/python -m pytest -q
```

## Required fixes

### SAST

`main.py` used a formatted SQL query in the book search route. The route now uses a parameterized `LIKE ?` query and passes the search text as a value. A regression test sends SQL-looking text and confirms it is treated as normal search text.

### Secrets

`main.py` no longer contains the two credential values. It reads `BOOKSTORE_API_KEY` and `BOOKSTORE_SECRET_TOKEN` from the environment instead. `.env.example` shows the required variable names, while `.env` stays ignored. The local Semgrep rule in `semgrep-local/rules.yml` checks for literal assignments to these names.

### SCA

`requirements.txt` now uses `requests==2.34.2` instead of the vulnerable `2.25.1` pin. The updated dependency audit reports no known vulnerabilities.

## Extra cleanup

I also replaced wildcard CORS with a localhost allowlist and disabled credential sharing. The frontend now creates paragraph nodes and sets `textContent` instead of placing review text in `innerHTML`.

## Results

The automatic Semgrep scan completed with zero findings. The local secret rule completed with zero findings. The dependency audit reported no known vulnerabilities. The test suite passed with 7 tests.
