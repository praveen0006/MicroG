# 02 — Getting Started

Prerequisites
- Python 3.10 or 3.11
- `pip`, virtualenv (recommended)

Install

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -e .
```

Basic run (local, small scale)

1. Prepare `config.yaml` (see `03_Configuration.md` for example).
2. Train for a single state (fastest):

```bash
python -m sales_forecast.training.cli --states California
```

Expected output:

```
Starting training run v20260506_175529 for 1 states
State California: 6 CV folds
State California done in 248.3s | top=['xgboost', 'lstm'] | weights={'xgboost': 0.65, 'lstm': 0.35}
Run v20260506_175529 complete. Promoted to current.
```

3. Launch API and dashboard (in separate terminals):

```bash
# Terminal 1: API
sales-forecast-api --port 8000
```

Expected output:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

```bash
# Terminal 2: Dashboard
streamlit run dashboard/streamlit_app.py
```

Expected output:

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Notes
- For CI and quick checks, skip heavy models (set `models.enabled` in `config.yaml`).
