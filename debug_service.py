from sales_forecast.config import load_config
from sales_forecast.api.service import ForecastService

cfg = load_config()
service = ForecastService(cfg)
service.reload()
print(f"Loaded version: {service.loaded_version}")
print(f"States available: {service.states_available()}")
print(f"Metadata states keys: {list(service.metadata.get('states', {}).keys())}")
