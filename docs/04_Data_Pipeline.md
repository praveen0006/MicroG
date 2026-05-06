# 04 — Data Pipeline

This page explains data ingestion, normalization, and preprocessing.

Loader: `src/sales_forecast/data/loader.py`
- Accepts `.xlsx` or `.csv`.
- Normalizes dates robustly and converts target to numeric.

Preprocessor: `src/sales_forecast/data/preprocessor.py`
- Resamples to weekly grid (`cfg.data.freq`, default `W-SUN`).
- Imputation steps:
  - Linear interpolation for short gaps
  - Forward-fill for medium gaps
  - Back-fill for leading NaNs
- Outlier handling: IQR + z-score; default strategy `cap`.

Example: load + preprocess

```python
from sales_forecast.config import load_config
from sales_forecast.data import DataLoader, Preprocessor

cfg = load_config()
df = DataLoader(cfg).load()
per_state = Preprocessor(cfg).transform(df)
print(list(per_state.keys())[:5])
print(per_state['California'].head())
```

Expected output:

```
['California', 'Texas', 'Florida', 'New York', 'Illinois']
                 sales  outlier_flag
date
2020-01-05     125000              0
2020-01-12     128500              0
2020-01-19     122000              0
2020-01-26     130000              0
2020-02-02     132000              0
```

Edge cases
- Ensure `date` strings are parseable (see `loader._parse_date`).
- Very short histories (< `min_history_weeks`) are skipped.
