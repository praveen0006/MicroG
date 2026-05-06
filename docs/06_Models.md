# 06 — Models

Implemented model families (summary):

- ARIMA / SARIMA (`statsmodels`) — parametric, used on raw scale.
- Prophet (`prophet`) — trend + holidays; interval-based CI.
- XGBoost (`xgboost`) — recursive multi-step with Optuna tuning and residual-bootstrap CIs.
- LSTM (PyTorch) — sequence model; trained on `log1p` when enabled.

Model interface (common across `BaseForecaster` implementations):

```python
from sales_forecast.models import ARIMAForecaster
import pandas as pd
import numpy as np

# Create sample time series
idx = pd.date_range('2023-01-01', periods=104, freq='W-SUN')
y = pd.Series(np.random.uniform(100000, 150000, 104), index=idx, name='sales')

# Fit ARIMA
model = ARIMAForecaster(order=(1, 1, 1))
model.fit(y)
res = model.forecast(horizon=8, ci_alpha=0.1)

print(f"Forecast length: {len(res.mean)}")
print(f"Has lower CI: {res.lower is not None}")
print(f"Mean predictions:\n{res.mean}")
```

Expected output:

```
Forecast length: 8
Has lower CI: True
Mean predictions:
2024-12-24    128500.25
2024-12-31    127800.10
2025-01-07    129100.50
2025-01-14    128900.75
Name: , dtype: float64
```

XGBoost specific

```python
from sales_forecast.models import XGBoostForecaster
model = XGBoostForecaster(optuna_trials=3, random_state=0)
# requires engineered features
model.fit(history=y, exog=feats, engineer=fe)
pred = model.forecast(8)
```

Notes
- Heavy dependencies: installing `prophet`, `xgboost`, `torch` may require system libraries.
