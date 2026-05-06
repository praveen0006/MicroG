# 07 — Training Pipeline

`TrainingPipeline.run()` orchestrates per-state model evaluation and artifact persistence.

Main steps per state
1. Build CV folds with `WalkForwardSplitter`.
2. For each fold, fit every enabled model and collect OOF predictions.
3. Compute metrics (RMSE, MAE, etc.) via `compute_metrics`.
4. Select top-K models by mean RMSE.
5. Compute ensemble weights (inverse_rmse, softmax, equal, or stacking).
6. Refit selected models on full history, save artifacts to registry.
7. (Optional) build SHAP explainability for XGBoost.

Example usage

```bash
python -m sales_forecast.training.cli --states California
```

Programmatic

```python
from sales_forecast.training.pipeline import TrainingPipeline
from sales_forecast.config import load_config

cfg = load_config()
pipe = TrainingPipeline(cfg)
report = pipe.run(states=["California"])

print(f"Registry version: {report.version}")
for state, sr in report.states.items():
    print(f"State: {state}")
    print(f"  Selected models: {sr.selected_models}")
    print(f"  Ensemble weights: {sr.ensemble_weights}")
    print(f"  Duration: {sr.duration_seconds:.1f}s")
```

Expected output:

```
Registry version: v20260506_175529
State: California
  Selected models: ['xgboost', 'lstm']
  Ensemble weights: {'xgboost': 0.65, 'lstm': 0.35}
  Duration: 245.3s
```

Outputs
- Per-state artifacts in `artifacts/registry/<version>/states/<state>/` including `*.joblib`, `conformal.json`, `cv_predictions.csv`.
