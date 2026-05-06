# 03 — Configuration

`config.yaml` controls all runtime parameters. Example minimal config snippet:

```yaml
project:
  name: sales-forecast
  random_seed: 42
data:
  source_path: data/raw/Sales.xlsx
  date_col: date
  state_col: state
  target_col: sales
features:
  target_transform: log1p
models:
  enabled: [arima, xgboost]
forecast:
  horizon_weeks: 8
```

Load programmatically:

```python
from sales_forecast.config import load_config

cfg = load_config()
print(f"Project: {cfg.project.name}")
print(f"Random seed: {cfg.project.random_seed}")
print(f"Models enabled: {cfg.models.enabled}")
print(f"Forecast horizon: {cfg.forecast.horizon_weeks} weeks")
print(f"CV folds: {cfg.cv.max_folds}")
```

Expected output:

```
Project: sales-forecast
Random seed: 42
Models enabled: ['arima', 'sarima', 'prophet', 'xgboost', 'lstm']
Forecast horizon: 8 weeks
CV folds: 6
```

Paths are resolved relative to the repo root if `config.yaml` is in the root.
