import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


LOCATIE = "Amsterdam"


try:
    from key import API_KEY  
except Exception:
    API_KEY = os.environ.get("WEERLIVE_API_KEY", "")  

if not API_KEY:
    st.error("Geen API key gevonden. Zet 'API_KEY' in key.py of export WEERLIVE_API_KEY.")
    st.stop()


@st.cache_data(ttl=600)
def fetch_hourly(locatie: str) -> pd.DataFrame:
    url = f"https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie={locatie}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    js = r.json()

    
    df = pd.DataFrame(js.get("uur_verw", []))

    if df.empty:
        raise ValueError("Geen uurlijkse data ontvangen ('uur_verw' leeg).")

   
    colmap = {
        "uur": "time",
        "tijd": "time",
        "temp": "temp_c",
        "neersl": "rain_mm",
        "neerslag": "rain_mm",
        "neerslag_mm": "rain_mm",
        "windkmh": "wind_kmh",
        "wind_kmh": "wind_kmh",
    }
    
    existing = {k: v for k, v in colmap.items() if k in df.columns}
    df = df.rename(columns=existing)

    
    needed = ["time", "temp_c", "rain_mm", "wind_kmh"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"Ontbrekende velden in API-respons: {missing}. Kolommen ontvangen: {list(df.columns)}")

  
    df = df.head(24).copy()

    
    df["time_label"] = df["time"].astype(str)

    
    for c in ["temp_c", "rain_mm", "wind_kmh"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    return df


st.title("Komende 24 uur — Weergrafiek")
st.caption(f"Locatie: {LOCATIE}")

try:
    df = fetch_hourly(LOCATIE)
except Exception as e:
    st.error(f"Kon data niet ophalen: {e}")
    st.stop()



col1, col2, col3 = st.columns(3)
with col1:
    show_temp = st.checkbox("Toon temperatuur (°C)", value=True)
with col2:
    show_rain = st.checkbox("Toon neerslag (mm)", value=True)
with col3:
    show_wind = st.checkbox("Toon wind (km/h)", value=True)

if not any([show_temp, show_rain, show_wind]):
    st.info("Selecteer ten minste één grootheid om te plotten.")
    st.stop()


fig, ax1 = plt.subplots(figsize=(12, 5))


df["time_label"] = df["time"].astype(str)


df["time_label"] = df["time_label"].str.extract(r"(\d{2}:\d{2})")


x = range(len(df))
ax1.set_xticks(x)
ax1.set_xticklabels(df["time_label"], rotation=45, ha="right")


handles, labels = [], []


line_temp = None
if show_temp:
    line_temp, = ax1.plot(x, df["temp_c"], linewidth=2, label="Temp (°C)", color='r')
    ax1.set_ylabel("Temperatuur (°C)")
else:
   
    ax1.yaxis.set_visible(False)
    ax1.spines["left"].set_visible(False)

ax2 = None
bars = None
if show_rain:
    ax2 = ax1.twinx()
    bars = ax2.bar(x, df["rain_mm"], alpha=0.3, label="Neerslag (mm)")
    ax2.set_ylabel("Neerslag (mm)")
else:
    
    pass


ax3 = None
line_wind = None
if show_wind:
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.15)) 
    line_wind, = ax3.plot(x, df["wind_kmh"], linestyle="--", linewidth=2, label="Wind (km/h)")
    ax3.set_ylabel("Wind (km/h)")
else:
   
    pass

def hide_axis(ax):
    if ax is None:
        return
    ax.yaxis.set_visible(True)
    for side in ["left", "right"]:
        if side in ax.spines:
            ax.spines[side].set_visible(True)
    ax.grid(True)


ax1.set_title("24-uurs verwachting " + LOCATIE + ": temperatuur, neerslag, wind")
from matplotlib.patches import Patch
if line_temp is not None:
    handles.append(line_temp)
    labels.append("Temp (°C)")
if bars is not None:
    handles.append(Patch(alpha=0.3))
    labels.append("Neerslag (mm)")
if line_wind is not None:
    handles.append(line_wind)
    labels.append("Wind (km/h)")

if handles:
    ax1.legend(handles, labels, loc="upper left")

plt.tight_layout()
st.pyplot(fig)
