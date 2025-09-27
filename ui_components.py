"""Streamlit UI helper functions."""
from typing import List, Dict, Any
import streamlit as st

def inject_min_style() -> None:
    st.markdown(
        "<style>.stApp{max-width:840px;margin:auto;} div.block-container{padding-top:1.5rem;}</style>",
        unsafe_allow_html=True,
    )

def render_current_block(now: Dict[str, Any], imperial: bool) -> None:
    place = f"{now.get('city','')}, {now.get('country','')}".strip(", ")
    st.subheader(place or "Current")
    cols = st.columns(4)
    unit_temp = "F" if imperial else "C"
    unit_wind = "mph" if imperial else "km/h"
    cols[0].metric("Now", _fmt_deg(now.get("temp_c"), unit_temp), help=now.get("desc") or "")
    cols[1].metric("Feels", _fmt_deg(now.get("feels_c"), unit_temp))
    cols[2].metric("Humidity", f"{now.get('humidity','n/a')}%")
    cols[3].metric("Wind", _fmt_num(now.get("wind_kph")) + f" {unit_wind}")

def render_forecast_list(rows: List[Dict[str, Any]], imperial: bool) -> None:
    st.markdown("**Next 24 hours**")
    unit_wind = "mph" if imperial else "km/h"
    for row in rows:
        c1, c2, c3, c4 = st.columns([2, 2, 4, 2])
        time_str = row.get("time","")
        c1.write(time_str.split(" ")[1] if " " in time_str else time_str)
        c2.write(_fmt_deg(row.get("temp_c"), "F" if imperial else "C"))
        c3.write(row.get("desc","n/a"))
        c4.write(_fmt_num(row.get("wind_kph")) + f" {unit_wind}")

def _fmt_deg(v, unit) -> str:
    return f"{round(v)}°{unit}" if isinstance(v, (int, float)) else "n/a"

def _fmt_num(v) -> str:
    return f"{round(v)}" if isinstance(v, (int, float)) else "n/a"
