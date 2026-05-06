# Sales Forecast Pro — Project Documentation

This document provides a developer-friendly overview of the project, setup instructions, API examples, and sample outputs to help you run, develop, and debug the system.

---

## 1. Overview

Sales Forecast Pro is a production-ready weekly per-state sales forecasting pipeline. It trains multiple model families (ARIMA, SARIMA, Prophet, XGBoost, LSTM), evaluates them using walk-forward CV, selects a top-K ensemble per state, and serves forecasts via a FastAPI backend and a Streamlit dashboard.

Key locations:

- Source: `src/sales_forecast`
- Config: `config.yaml`
- Packaging: `pyproject.toml`
- Artifacts / registry: `artifacts/registry`

---

## 2. Quick Start

1. Install (recommended inside a virtualenv):

```bash
git clone https://github.com/praveen0006/MicroG.git
cd MicroG
pip install -e .
```

2. Train (example: California):

```bash
# Using the provided console script (installed by pip install -e .)
sales-forecast-train --states California

# or via module entrypoint
python -m sales_forecast.training.cli --states California
```

3. Start the API and dashboard:

```bash
# Start API (uvicorn/entrypoint)
sales-forecast-api --port 8000

# Start Streamlit dashboard
streamlit run dashboard/streamlit_app.py
```

Notes: Training writes a versioned registry under the configured artifacts directory. The API loads the `current` registry by reading the manifest.json in the registry root.

---

## 3. API Reference & Examples

The FastAPI app is defined in `src/sales_forecast/api/app.py` and exposes these important endpoints:

- `GET /health` — service health and loaded registry version.
- `POST /train` — trigger a background training job.
- `GET /train/{job_id}` — query training status.
- `GET /predict` — get forecast for a state (requires trained registry).
- `GET /predict/breakdown` — ensemble + per-member forecasts.
- `GET /backtest` — saved CV predictions and metrics.
- `POST /report` — generate a PDF report.

Example: Request a forecast (requires that a registry is loaded):

```bash
curl -sS "http://localhost:8000/predict?state=California&horizon=8" | jq
```

Sample response (trimmed):

```json
{
  "state": "California",
  "registry_version": "v20260506_175529",
  "horizon_weeks": 8,
  "selected_models": ["xgboost", "lstm"],
  "ensemble_weights": {"xgboost": 0.7, "lstm": 0.3},
  "ci_method": "conformal",
  "forecast": [
    {"date":"2026-05-10","yhat":12345.0,"yhat_lower":11800.0,"yhat_upper":12900.0},
    {"date":"2026-05-17","yhat":12450.0,"yhat_lower":11900.0,"yhat_upper":13000.0}
  ],
  "drift": null
}
```

If no registry is loaded the API will return HTTP 503 with a message: `No trained model registry is loaded. Call POST /train first.`

---

## 4. Developer Guide — Key Components

- Configuration (`src/sales_forecast/config/settings.py`): Typed config using Pydantic v2. Use `load_config()` to read `config.yaml` and resolve project paths.

- Data loader (`src/sales_forecast/data/loader.py`): Reads Excel/CSV and normalizes columns. Important: date parsing is robust but watch for edge-case formats.

- Preprocessing (`src/sales_forecast/data/preprocessor.py`): Resamples to weekly grid, imputes gaps, caps/flags outliers.

- Feature engineering (`src/sales_forecast/features/engineer.py`): Produces lags, rolling stats, calendar, Fourier, and holiday features. The `FeatureEngineer` stores fit-time artifacts used during forecasting.

- Models (`src/sales_forecast/models`): Implementations of ARIMA, SARIMA, Prophet, XGBoost (Optuna hyperparameter tuning + recursive forecasting), LSTM (PyTorch). Model factory is `models/registry.py`.

- Training pipeline (`src/sales_forecast/training/pipeline.py`): Walk-forward CV, per-fold OOF predictions, ranking by RMSE, ensembling (inverse_rmse/stacking), final refit, saving artifacts + conformal calibrators.

- Service layer (`src/sales_forecast/api/service.py`): Loads model artifacts, applies `FeatureEngineer`, performs per-member forecasts, builds ensemble via `WeightedEnsemble`, sanitizes numeric issues, and exposes high-level calls for the API.

- Registry (`src/sales_forecast/utils/versioning.py`): Filesystem registry with `manifest.json` tracking `current` version and per-version `states/<state>/` artifacts.

---

## 5. Running Tests & Static Checks

Run unit tests:

```bash
pytest -q
```

Run the linter (ruff):

```bash
ruff src tests
```

Run type checks (mypy):

```bash
mypy src --ignore-missing-imports
```

Notes: Tests use `tests/conftest.py` fixtures which redirect artifact directories to temporary folders.

---

## 6. Troubleshooting & Known Issues

- Date parsing: older code used an invalid `isinstance` expression that raises a `TypeError` on some Python versions. The corrected check uses a tuple, e.g. `isinstance(value, (datetime, pd.Timestamp))`. The code location is: [src/sales_forecast/data/loader.py](src/sales_forecast/data/loader.py#L75).

- Heavy dependencies: packages like `prophet`, `xgboost`, and `torch` can be heavy to install and may require system libraries. For CI or quick tests, consider mocking or pinning lighter alternatives.

- Broad exception handling: training and API layers sometimes catch broad `Exception`, which can hide underlying errors. When debugging, inspect logs (`project.log_dir`) for full tracebacks.

---

## 7. Recommended Next Steps

1. Run `pytest` and `ruff` and fix any test/lint failures.
2. Add CI (GitHub Actions): install minimal deps for unit tests (skip heavy ML deps) and run smoke tests.
3. Improve observability: surface training logs into a central `train.log` and add API request tracing.
4. Tighten exception handling in `api/app.py` and `training/pipeline.py` to avoid masking root causes.

---

## 8. Contact / Further Help

If you want, I can:

- Run `pytest` in this workspace and report failures.
- Create a GitHub Actions CI workflow that runs lint/tests (fast profile without heavy ML deps).
- Patch the `isinstance` bug automatically and run tests.

Tell me which of the above you'd like me to do next.
