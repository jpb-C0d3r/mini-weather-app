# Streamlit Weather — OpenWeatherMap Edition

A small, modular Streamlit app that shows current conditions and the next 24-hour forecast using the OpenWeatherMap API.

---

## Features
- City search using OpenWeather geocoding, current weather, and 5-day/3-hour forecast trimmed to the next 8 slots (~24h)
- Units toggle: Metric (°C, km/h) or Imperial (°F, mph)
- 5-minute caching for repeated requests
- Simple retries for transient HTTP failures
- Clean, compact UI for “Now” metrics and a 24-hour list

---

## Repo Structure
app.py               — Streamlit entrypoint and page layout  
openweather.py       — OWM client: geocode/current/forecast + parse helpers  
ui_components.py     — Render blocks for current and next-24h  
units.py             — °C↔°F, m/s→km/h, km/h→mph  
requirements.txt     — Streamlit + Requests

---

## Quick Start

1) Set your OpenWeather API key

Option A — Streamlit secrets (preferred)  
Create file: .streamlit/secrets.toml  
Contents: OPENWEATHER_API_KEY = "your-key"

Option B — Environment variable  
Linux/macOS: export OPENWEATHER_API_KEY="your-key"  
Windows PowerShell: $env:OPENWEATHER_API_KEY="your-key"

2) Install and run

pip install -r requirements.txt  
streamlit run app.py

---

## How it Works

app.py  
- Reads the API key via config.get_api_key()  
- Renders a city search form and units toggle  
- Calls geocoding, current, and forecast endpoints  
- Converts units when needed  
- Renders UI blocks for “Now” and next-24h

openweather.py  
- Wraps three endpoints with small retry loops and 300s caching  
  • Geocode: GET /geo/1.0/direct → {lat, lon}  
  • Current: GET /data/2.5/weather → parse_current()  
  • Forecast: GET /data/2.5/forecast (3-hour steps) → parse_next_24h() returning the first 8 items

ui_components.py  
- inject_min_style() for minimal page styling  
- Metrics block: city, country, temp, feels, humidity, wind  
- Next-24h list: time, temperature, description, wind

units.py  
- c_to_f, ms_to_kph, kph_to_mph

---

## Configuration Notes
- Ensure config.get_api_key() returns a non-empty key  
- It should check Streamlit secrets first, then the OPENWEATHER_API_KEY environment variable

---

## Dependencies
streamlit==1.38.0  
requests>=2.31.0

Install with: pip install -r requirements.txt

---

## Error Handling
- Network and server errors surface as Streamlit messages  
- HTTP 5xx triggers retries before failing

---

## Limitations
- Forecast view limited to the next ~24 hours (first 8 forecast entries)  
- Simple city text search only; no multi-match disambiguation
