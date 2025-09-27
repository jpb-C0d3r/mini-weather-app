"""
OpenWeatherMap client functions: geocode, current, forecast.
Includes retries and caching.
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional

import requests
import streamlit as st
from units import ms_to_kph

OWM_GEOCODE = "https://api.openweathermap.org/geo/1.0/direct"
OWM_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

def _req_get(url: str, params: Dict[str, Any], retries: int = 3, timeout: int = 8) -> requests.Response:
    for i in range(retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            if r.status_code >= 500:
                raise requests.RequestException(f"server {r.status_code}")
            return r
        except requests.RequestException:
            if i == retries - 1:
                raise
            time.sleep(0.8 * (2 ** i))
    raise RuntimeError("unreachable")

@st.cache_data(show_spinner=False, ttl=300)
def geocode_city(city: str, api_key: str) -> Optional[Dict[str, float]]:
    r = _req_get(OWM_GEOCODE, {"q": city, "limit": 1, "appid": api_key})
    r.raise_for_status()
    arr = r.json()
    if not arr:
        return None
    return {"lat": arr[0]["lat"], "lon": arr[0]["lon"]}

@st.cache_data(show_spinner=False, ttl=300)
def fetch_current(lat: float, lon: float, api_key: str) -> Dict[str, Any]:
    r = _req_get(OWM_WEATHER, {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"})
    r.raise_for_status()
    return r.json()

@st.cache_data(show_spinner=False, ttl=300)
def fetch_forecast(lat: float, lon: float, api_key: str) -> Dict[str, Any]:
    r = _req_get(OWM_FORECAST, {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "cnt": 10})
    r.raise_for_status()
    return r.json()

def parse_current(data: Dict[str, Any]) -> Dict[str, Any]:
    w = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})
    return {
        "desc": w.get("description", "n/a").title(),
        "icon": w.get("icon"),
        "temp_c": main.get("temp"),
        "feels_c": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "wind_kph": ms_to_kph(wind.get("speed", 0.0)),
        "city": data.get("name", ""),
        "country": data.get("sys", {}).get("country", ""),
    }

def parse_next_24h(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    for item in data.get("list", [])[:8]:
        w = item.get("weather", [{}])[0]
        main = item.get("main", {})
        wind = item.get("wind", {})
        out.append({
            "time": item.get("dt_txt", ""),
            "temp_c": main.get("temp"),
            "desc": w.get("description", "n/a").title(),
            "icon": w.get("icon"),
            "wind_kph": ms_to_kph(wind.get("speed", 0.0)),
        })
    return out
