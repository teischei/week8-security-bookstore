# Baseline scan

## Commands

```bash
.semgrep-venv/bin/semgrep scan --config auto
.semgrep-venv/bin/semgrep scan --config p/secrets
.venv/bin/pip-audit -r requirements.txt
```

## Results

The automatic Semgrep scan completed with three findings. It found the wildcard CORS setting once and the formatted SQL query twice with two different rules.

The dedicated Semgrep secrets rules returned zero findings. The starter still contains a fake hardcoded key, so this showed that the public rules did not recognize that test value. I kept this result because a clean scanner result does not mean the source is safe.

The dependency audit found 24 known vulnerabilities in three packages. The outdated `requests==2.25.1` pin brought in old versions of `idna` and `urllib3`.

## Triage plan

I will fix one issue in each required category.

- SAST with a parameterized SQL query
- Secrets by moving the values to environment variables
- SCA by upgrading the requests dependency

I will also fix the wildcard CORS setting and the frontend XSS sink so the final Semgrep scan is clean. The prompt injection endpoint will be demonstrated and mitigated separately.
