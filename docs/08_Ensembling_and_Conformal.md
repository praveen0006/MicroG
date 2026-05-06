# 08 — Ensembling & Conformal

Ensembling
- `WeightedEnsemble` computes weighted combination of per-model means.
- Weighting schemes: `inverse_rmse`, `softmax`, `equal`, `stacking` (ridge-simplex).

Stacking
- Uses OOF predictions to fit a small meta-learner (`StackingMetaLearner`) with simplex constraints.

Split-Conformal CIs
- Calibration created from residuals across CV folds per horizon step.
- Stored as `conformal.json` with `half_widths` per-horizon.
- At predict time the `ConformalCalibrator` is applied to member forecasts to produce valid finite-sample CIs.

Sample: compute ensemble in code

```python
from sales_forecast.models.ensemble import WeightedEnsemble
from sales_forecast.models import ForecastResult
import pandas as pd
import numpy as np

# Create sample forecasts from two models
idx = pd.date_range('2026-05-10', periods=8, freq='W-SUN')
mean1 = pd.Series([135000, 136500, 134800, 137200, 135900, 138100, 136500, 137800], index=idx)
mean2 = pd.Series([134500, 135800, 135200, 136800, 135500, 137800, 136200, 137500], index=idx)

res1 = ForecastResult(mean=mean1, lower=None, upper=None, metadata={})
res2 = ForecastResult(mean=mean2, lower=None, upper=None, metadata={})

ens = WeightedEnsemble({"xgboost": 0.65, "lstm": 0.35})
combined = ens.combine({"xgboost": res1, "lstm": res2})

print(f"Combined forecast (first 3 points):")
print(combined.mean.head(3))
```

Expected output:

```
Combined forecast (first 3 points):
2026-05-10    134825.0
2026-05-17    136275.0
2026-05-24    134940.0
Name: , dtype: float64
```
