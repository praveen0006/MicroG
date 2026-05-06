# 05 — Feature Engineering

`FeatureEngineer` creates all features used by ML/DL models.

Features produced
- Lags: `lag_1`, `lag_7`, `lag_14`, ...
- Rolling: `roll_mean_{w}`, `roll_std_{w}` computed on lag-1
- Calendar: `week`, `month`, `quarter`, `year`
- Trend: `trend_lin`, and changepoint basis `cp_{i}`
- Fourier: `fy_sin_k`, `fy_cos_k`, `fq_sin_k`, `fq_cos_k`
- Holidays: `holiday_in_week`, `days_to_next_holiday`

Usage during training

```python
from sales_forecast.features import FeatureEngineer
import pandas as pd
import numpy as np

fe = FeatureEngineer(cfg, state="California")
# Example series: 52 weeks of data
idx = pd.date_range('2023-01-01', periods=52, freq='W-SUN')
y_series = pd.Series(np.random.uniform(100000, 150000, 52), index=idx)
feats = fe.fit_transform(y_series.to_frame("y"), target_col="y")
X = feats[fe.artifacts.feature_columns]
print(f"Features shape: {X.shape}")
print(f"Columns: {list(X.columns)[:10]}")
```

Expected output:

```
Features shape: (52, 34)
Columns: ['lag_1', 'lag_7', 'lag_14', 'lag_30', 'roll_mean_4', 'roll_std_4', 'roll_mean_8', 'roll_std_8', 'week', 'month']
```

Recursive forecasting
- `FeatureEngineer.transform_for_forecast()` supports stepwise recursive forecasts used by XGBoost/LSTM.
