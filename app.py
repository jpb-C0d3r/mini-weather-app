"""Streamlit Weather — Modular, flat structure, OpenWeatherMap edition."""
import requests
import streamlit as st

from config import get_api_key
from units import c_to_f, kph_to_mph
from openweather import geocode_city, fetch_current, fetch_forecast, parse_current, parse_next_24h
from ui_components import inject_min_style, render_current_block, render_forecast_list

st.set_page_config(page_title="Weather", page_icon="⛅", layout="centered")
inject_min_style()
st.title("Weather")

api_key = get_api_key()

with st.form("city_form"):
    city = st.text_input("City", placeholder="e.g., Manila")
    units = st.selectbox("Units", ["Metric (°C, km/h)", "Imperial (°F, mph)"])
    submitted = st.form_submit_button("Get weather")

if submitted:
    city_clean = city.strip()
    if not city_clean:
        st.error("City is required.")
        st.stop()
    try:
        geo = geocode_city(city_clean, api_key)
        if not geo:
            st.warning("City not found. Try another spelling.")
            st.stop()

        cur_json = fetch_current(geo["lat"], geo["lon"], api_key)
        fc_json = fetch_forecast(geo["lat"], geo["lon"], api_key)

        now = parse_current(cur_json)
        next24 = parse_next_24h(fc_json)

        use_imperial = units.startswith("Imperial")
        if use_imperial:
            now["temp_c"] = c_to_f(now["temp_c"])
            now["feels_c"] = c_to_f(now["feels_c"])
            now["wind_kph"] = kph_to_mph(now["wind_kph"])
            for r in next24:
                r["temp_c"] = c_to_f(r["temp_c"])
                r["wind_kph"] = kph_to_mph(r["wind_kph"])

        render_current_block(now, use_imperial)
        render_forecast_list(next24, use_imperial)
        st.caption("Data: OpenWeatherMap (Geocoding, Current, 5-day/3-hour Forecast)")

    except requests.HTTPError as e:
        st.error(f"Provider error: {e.response.status_code if e.response else 'HTTP'}")
    except requests.RequestException:
        st.error("Network error.")
    except Exception as ex:
        st.error(f"Unexpected error: {type(ex).__name__}")
