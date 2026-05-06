# 10 — Dashboard (Streamlit)

The Streamlit UI is in `dashboard/streamlit_app.py`.

Start locally:

```bash
streamlit run dashboard/streamlit_app.py
```

Expected terminal output:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501

  For better performance, install watchdog:
  $ pip install watchdog
```

Example interaction (programmatically):

```python
import requests

# Query available states from API
resp = requests.get("http://localhost:8000/states")
states = resp.json()['states']
print(f"Available states: {states[:5]}")

# Get a forecast to display in dashboard
resp = requests.get(
    "http://localhost:8000/predict",
    params={"state": "California", "horizon": 8}
)
forecast_data = resp.json()
print(f"Forecast for {forecast_data['state']}: {len(forecast_data['forecast'])} weeks")
```

Expected output:

```
Available states: ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California']
Forecast for California: 8 weeks
```
