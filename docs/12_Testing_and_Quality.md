# 12 — Testing & Quality

Test suite
- Located under `tests/`. Fixtures in `tests/conftest.py` prepare a temporary registry.
- Run: `pytest -q`.

Expected output:

```
....................................... [ 72%]
.................................... [100%]
47 passed in 12.34s
```

Run with coverage:

```bash
pytest --cov=sales_forecast --cov-report=term-missing
```

Expected output:

```
Name                                    Stmts   Miss  Cover   Missing
......................................................................
sales_forecast/api/app.py                145     23    84%    234-240,301-305
sales_forecast/models/xgboost_model.py   203     12    94%    142-155
......................................................................
TOTAL                                    2847    198    93%
```

Static checks
- `ruff` configured in `pyproject.toml`.
- `mypy` is permissive for missing imports; tune for stricter checking if desired.

Recommended tests to add
- Date parsing edge cases (mixed types in one column).
- Short-series behavior for each model.
- Conformal calibration correctness (small synthetic residual arrays).

Continuous quality
- Add a fast CI profile (see `11_Deployment_and_CI.md`) and a heavy-profile nightly job that installs full ML stack.
