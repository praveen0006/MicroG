# 11 — Deployment & CI

Lightweight CI recipe (GitHub Actions) idea:

1. Use a fast test matrix that installs minimal dev deps (skip `prophet`, `torch`, `xgboost`).
2. Run `ruff`, `mypy` (fast profile), and `pytest` with markers that skip heavy tests.

Example Actions job (sketch):

```yaml
name: CI
on: [push, pull_request]
jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -e .[dev]
      - run: ruff src tests
      - run: mypy src --ignore-missing-imports
      - run: pytest -q
```

Expected output in Actions log:

```
✓ ruff src tests (0.08s)
✓ mypy src (1.23s) - No issues found
✓ pytest -q (15.42s) - 47 passed
```

Containerization
- `Dockerfile` and `docker-compose.yml` exist; for production pin base images and install system deps for `prophet`/`torch`.

Production notes
- Use `uvicorn` behind a process manager (systemd or container orchestrator).
- Mount `artifacts/registry` from a persistent store.
