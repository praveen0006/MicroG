# 13 — Troubleshooting & Examples

This page collects common issues, fixes, and runnable examples with sample outputs.

1) Date parsing error (known bug)

Problem: using `isinstance(value, datetime | pd.Timestamp)` raises `TypeError`.

Fix: replace with:

```python
from datetime import datetime
import pandas as pd

if isinstance(value, (datetime, pd.Timestamp)):
    return pd.Timestamp(value)
```

Location: `src/sales_forecast/data/loader.py` (see line referenced in diagnostics).

2) Example: request a forecast via Python

```python
import requests
resp = requests.get('http://localhost:8000/predict', params={'state':'California','horizon':8})
print(resp.json())
```

Expected trimmed output:

```json
{"state":"California","horizon_weeks":8,"selected_models":["xgboost","lstm"]}
```

3) If training fails with OOM or long runtimes

- Reduce `cfg.models.xgboost.optuna_trials` and `cfg.models.lstm.epochs` for debugging.
- Use a single-state run via `--states` to iterate quickly.

Example: fast debug config

```yaml
models:
  enabled: [arima, xgboost]  # skip heavy models
xgboost:
  optuna_trials: 5           # from 30
models:
  lstm:
    epochs: 10               # from 80
ci:
  max_folds: 3              # from 6
```

4) Logs

- API logs: configured `api.log` under `project.log_dir`.
- Training logs: `train.log` in the same dir.

5) Ask me to run diagnostics

- I can patch the `isinstance` bug, run `pytest`, and report failures.
