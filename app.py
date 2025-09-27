import requests
import streamlit as st

WTTR_URL = "https://wttr.in/{}?format=j1"  # j1 = JSON format

st.set_page_config(page_title="Weather", page_icon="⛅", layout="centered")
st.title("Weather")

# 1) Input
city = st.text_input("City", value="", placeholder="e.g., Manila")

# 2) Action button
if st.button("Get weather"):
    # 2a) Basic validation
    city_clean = city.strip()
    if not city_clean:
        st.error("Please enter a city.")
    else:
        try:
            # 3) Fetch data
            resp = requests.get(WTTR_URL.format(city_clean), timeout=8)
            resp.raise_for_status()  # raise error for 4xx/5xx
            data = resp.json()

            # 4) Parse minimal fields from JSON
            # wttr.in JSON structure: current_condition is a list with one dict
            cc = data["current_condition"][0]
            temp_c = cc.get("temp_C", "?")
            feels_c = cc.get("FeelsLikeC", "?")
            humidity = cc.get("humidity", "?")
            wind_kmph = cc.get("windspeedKmph", "?")
            desc = cc.get("weatherDesc", [{"value": "No description"}])[0]["value"]

            # 5) Show results
            st.subheader(desc)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Temperature (°C)", temp_c)
                st.metric("Feels like (°C)", feels_c)
            with col2:
                st.metric("Humidity (%)", humidity)
                st.metric("Wind (km/h)", wind_kmph)

            st.caption("Source: wttr.in")
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException:
            st.error("Network error. Try again.")
        except (KeyError, IndexError, ValueError):
            st.error("Unexpected response. Try a different city.")
