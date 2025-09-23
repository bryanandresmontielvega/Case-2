from key import API_KEY
import json
import requests
import pandas as pd
import streamlit as st
import time


# ======================== API ========================
print(f'API_KEY: {API_KEY}')
location = "Maastricht"

url_string = f'https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie={location}'
print(url_string)
response = requests.get(url_string)

json_data = response.json()


# ======================== dataframes ========================
live_weer_df = pd.DataFrame(json_data["liveweer"])
dagverwachting_df = pd.DataFrame(json_data["wk_verw"])
uursverwachting_df = pd.DataFrame(json_data["uur_verw"])


# ======================== code ========================
def request_data_location(location='Amsterdam', key=API_KEY):
    url_string = f'https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie={location}'

    response = requests.get(url_string)
    json_data = response.json()

    live_weer_df = pd.DataFrame(json_data["liveweer"])
    dagverwachting_df = pd.DataFrame(json_data["wk_verw"])
    uursverwachting_df = pd.DataFrame(json_data["uur_verw"])

    return live_weer_df, dagverwachting_df, uursverwachting_df


# _, _, var = request_data_location(location='Mook')
# print(var)


# ======================== code ========================

# titel
st.title(f"Actueel Weer in {str(live_weer_df['plaats'][0])}")
st.caption(f"Weer laatst ge-update: {live_weer_df['time'][0]}")

# ======================== main weer cols ========================
st.subheader("Vandaag in beeld")
col01, col02, _, _, _, _  = st.columns(6)

col01.image(f"{live_weer_df['image'][0]}.png")
col02.caption(f"Het is nu {live_weer_df['samenv'][0]}")

st.caption(f"{live_weer_df['verw'][0]}")

st.subheader("Algemeen weer")
col1, col2, col3 = st.columns(3)

col1.metric(
        "Actuele temperatuur", 
        f"{float(live_weer_df['temp'].iloc[0])} °C", 
        f"Gevoel: {float(live_weer_df['gtemp'].iloc[0])} °C",
        delta_color="off",
        border=True)
col2.metric(
        "Luchtvochtigheid", 
        f"{float(live_weer_df['lv'].iloc[0])} %", 
        f"Dauwpunt: {float(live_weer_df['dauwp'].iloc[0])} °C",
        delta_color="off",
        border=True)
col3.metric(
        "Luchtdruk", 
        f"{float(live_weer_df['temp'].iloc[0])} mbar", 
        border=True)


st.subheader("Wind")
col5, col6, col7 = st.columns(3)

col5.metric(
    "Windrichting",
    f"{str(live_weer_df['windr'].iloc[0])}", 
    f"Richting: {int(live_weer_df['windrgr'].iloc[0])} °",
    delta_color="off",
    border=True
)
col6.metric(
    "Windsnelheid",
    f"{float(live_weer_df['windkmh'].iloc[0])} km/u", 
    f"{float(live_weer_df['windms'].iloc[0])} m/s",
    delta_color="off",
    border=True
)
col7.metric(
    "Windkracht (Beaufort)",
    f"{int(live_weer_df['windbft'].iloc[0])} bf", 
    f"{int(live_weer_df['windknp'].iloc[0])} kn", 
    delta_color="off",
    border=True
)

