# 09 — API & Service

FastAPI application factory: `src/sales_forecast/api/app.py`

Key endpoints
- `GET /health` — health and registry version
- `POST /train` — background training job
- `GET /predict` — retrieve forecast

Example: programmatic client

```python
import requests
import json

# Health check
resp = requests.get("http://localhost:8000/health")
print("Health:", resp.json())

# Get a forecast
resp = requests.get(
    "http://localhost:8000/predict",
    params={"state": "California", "horizon": 8, "ci_alpha": 0.1}
)
resp.raise_for_status()
data = resp.json()
print(json.dumps(data, indent=2))
```

Expected output:

```json
{
  "state": "California",
  "registry_version": "v20260506_175529",
  "horizon_weeks": 8,
  "selected_models": ["xgboost", "lstm"],
  "ensemble_weights": {"xgboost": 0.65, "lstm": 0.35},
  "ci_method": "conformal",
  "forecast": [
    {"date": "2026-05-10", "yhat": 135000.0, "yhat_lower": 130000.0, "yhat_upper": 140000.0},
    {"date": "2026-05-17", "yhat": 136500.0, "yhat_lower": 131200.0, "yhat_upper": 141800.0},
    {"date": "2026-05-24", "yhat": 134800.0, "yhat_lower": 129500.0, "yhat_upper": 140100.0}
  ],
  "drift": null
}
```

Service layer
- `ForecastService` loads artifacts via `ModelRegistry`, creates `StateBundle` objects and executes forecasts.
- Handles sanitization of NaN/Inf values and applies conformal calibrators when present.

Prometheus metrics
- If `prometheus_client` is available and enabled in config, the API exposes `/metrics/prom`.

Error handling
- 404: unknown state or missing artifacts
- 503: no registry loaded or missing artifacts
- 500: internal errors; inspect `api.log` in configured `project.log_dir`.
