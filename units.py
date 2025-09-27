"""Unit conversions for temperature and wind speed."""
from typing import Optional

def c_to_f(c: Optional[float]) -> Optional[float]:
    return None if c is None else (c * 9 / 5) + 32

def ms_to_kph(ms: Optional[float]) -> Optional[float]:
    return None if ms is None else ms * 3.6

def kph_to_mph(kph: Optional[float]) -> Optional[float]:
    return None if kph is None else kph * 0.621371
