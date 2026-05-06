# 01 — Project Overview

This page gives a high-level description of Sales Forecast Pro: goals, components, and quick diagrams.

Purpose
- Produce 8-week weekly sales forecasts per US state.
- Benchmark 5 model families and build a small ensemble per state.
- Provide a FastAPI backend and Streamlit dashboard for users.

High-level components
- `data/` — raw data ingestion and per-state weekly aggregation.
- `src/sales_forecast` — application code (data, features, models, training, api, utils).
- `artifacts/` — model registry; versioned outputs from training.

Quick architecture (textual)

1. Raw sales -> `DataLoader` -> per-state weekly series
2. `Preprocessor` cleans and imputes
3. `FeatureEngineer` creates lags, rolling stats, Fourier, holidays
4. `TrainingPipeline` runs walk-forward CV across models
5. Top-K models selected -> ensemble weights computed
6. Artifacts saved to `artifacts/registry/v...`
7. `ForecastService` loads artifacts for serving via FastAPI

Example: end-to-end programmatic flow

```python
from sales_forecast.config import load_config
from sales_forecast.training.pipeline import TrainingPipeline
from sales_forecast.api.service import ForecastService

# 1. Load config and train
cfg = load_config()
pipe = TrainingPipeline(cfg)
report = pipe.run(states=["California"])
print(f"Trained version: {report.version}")

# 2. Serve forecast
service = ForecastService(cfg)
service.reload()
result = service.predict(state="California", horizon=8)
print(f"Forecast states: {result['state']}")
print(f"Selected models: {result['selected_models']}")
```

Expected output:

```
Trained version: v20260506_175529
Forecast state: California
Selected models: ['xgboost', 'lstm']
```
