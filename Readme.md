## OpenWeatherMap upgrade

This app uses OpenWeatherMap with an API key.

### Setup the key
Option A — Streamlit secrets (preferred):

.streamlit/secrets.toml

OPENWEATHER_API_KEY = "your-key"


Option B — Environment variable:


export OPENWEATHER_API_KEY="your-key"

Windows PowerShell: $env:OPENWEATHER_API_KEY="your-key"

### Run


pip install -r requirements.txt
streamlit run app.py


### Notes
- Geocoding → current conditions → next-24h forecast.
- Caching 5 minutes. Simple retries for transient failures.

- Units toggle: Metric or Imperial.
