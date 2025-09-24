# %%
from key import API_KEY
import json
import requests
import streamlit as st 
import pandas as pd


# %%
# API key voor data opvragen
print(f'API_KEY: {API_KEY}')

# %%
url_string = f'https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie=Amsterdam'
print(url_string)
response = requests.get(url_string)

# Parse JSON
json_data = response.json()

live_weer_df = pd.DataFrame(json_data["liveweer"])
dagverwachting_df = pd.DataFrame(json_data["wk_verw"])
uursverwachting_df = pd.DataFrame(json_data["uur_verw"])


# dagverwachting_df = {
#     "dag": ["22-09-2025", "23-09-2025", "24-09-2025", "25-09-2025", "26-09-2025"],
#     "image": ["zon", "halfbewolkt", "regen", "bewolkt", "zon"],
#     "max_temp": [20, 17, 15, 16, 22],
#     "min_temp": [12, 10, 9, 9, 13],
#     "windbft": [3, 2, 5, 3, 2],
#     "windkmh": [14, 10, 25, 14, 12],
#     "windknp": [8, 6, 14, 8, 7],
#     "windms": [4, 3, 7, 4, 3],
#     "windrgr": [18, 34, 43, 52, 55],
#     "windr": ["NO", "NO", "ZW", "NO", "O"],
#     "neersl_perc_dag": [0, 20, 80, 40, 0],
#     "zond_perc_dag": [80, 47, 10, 25, 90],
# }


dagverwachting_df = pd.DataFrame(dagverwachting_df)




# %%
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1532767153582-b1a0e5145009?q=80&w=2814&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Weekdagen labels toevoegen (kort: ma, di, wo...)
dagverwachting_df["dag_vd_week"] = pd.to_datetime(
    dagverwachting_df["dag"], dayfirst=True
).dt.strftime("%a")

# Session state voor dagindex
if "dag_index" not in st.session_state:
    st.session_state["dag_index"] = 0
    
# Weertype icoontjes
weer_icons = {
    "zon": "☀️",
    "halfbewolkt": "⛅",
    "bewolkt": "☁️",
    "regen": "🌧️",
    "onweer": "⛈️",
    "sneeuw": "❄️"
}

# Kleurthema afhankelijk van weer
theme_colors = {
    "zon": "linear-gradient(150deg, #FFD500, #F2F5F1)",
    "halfbewolkt": "linear-gradient(135deg, #87CEEB, #FFFFFF)",
    "bewolkt": "linear-gradient(135deg, #B0C4DE, #F0F0F0)",
    "regen": "linear-gradient(135deg, #00BFFF, #F0F0F0)",
    "onweer": "linear-gradient(135deg, #708090, #2F4F4F)",
    "sneeuw": "linear-gradient(135deg, #E0FFFF, #FFFFFF)",
}

# Navigatieknoppen
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("◀️"):
        if st.session_state["dag_index"] > 0:
            st.session_state["dag_index"] -= 1
with col3:
    if st.button("▶️"):
        if st.session_state["dag_index"] < len(dagverwachting_df) - 1:
            st.session_state["dag_index"] += 1

# Weekdagen lijst
weekdagen = dagverwachting_df["dag_vd_week"].tolist()

# Slider (gekoppeld aan dag_index)
chosen_day = st.select_slider(
    "Kies een dag",
    options=weekdagen,
    value=weekdagen[st.session_state["dag_index"]],
    label_visibility="collapsed"
)

# Synchronisatie: alleen updaten als slider is aangepast
if chosen_day != weekdagen[st.session_state["dag_index"]]:
    st.session_state["dag_index"] = weekdagen.index(chosen_day)

# Geselecteerde dag ophalen
selected_day = dagverwachting_df.iloc[st.session_state["dag_index"]]
icon = weer_icons.get(selected_day["image"], "🌤️")
bg_color = theme_colors.get(selected_day["image"], "linear-gradient(135deg, #89CFF0, #FFFFFF)")

# Weerkaartje (app-stijl)
st.markdown(
    f"""
    <div style="padding:20px; border-radius:30px; background:{bg_color}; 
                box-shadow: 0px 4px 12px rgba(0,0,0,0.15); text-align:center; color:black;">
        <h2 style="margin-bottom:10px;">{icon} Weer op {selected_day['dag_vd_week']} {selected_day['dag']}</h2>

        
    <div style="padding:20px; border-radius:30px; background:{bg_color}; 
                box-shadow: 0px 4px 12px rgba(0,0,0,0.15); text-align:center; color:black;">
        <p style="font-size:20px; margin:5px;">🌡️ <b>Max:</b> {selected_day['max_temp']}°C</p>
        <p style="font-size:20px; margin:5px;">🌡️ <b>Min:</b> {selected_day['min_temp']}°C</p>
        <p style="font-size:20px; margin:5px;">💨 <b>Wind:</b> {selected_day['windbft']} Bft ({selected_day['windkmh']} km/h, {selected_day['windr']})</p>
        <p style="font-size:20px; margin:5px;">☔ <b>Kans op regen:</b> {selected_day['neersl_perc_dag']}%</p>
        <p style="font-size:20px; margin:5px;">☀️ <b>Zonkans:</b> {selected_day['zond_perc_dag']}%</p>
    </div>
    """,
    unsafe_allow_html=True
)



#%%
# %%
#tweede versie
# dagverwachting_df = pd.DataFrame(dagverwachting_df)




# %%
# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-image: url('https://images.unsplash.com/photo-1532767153582-b1a0e5145009?q=80&w=2814&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
#         background-size: cover;
#         background-attachment: fixed;
#         background-position: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# # Weekdagen labels toevoegen (kort: ma, di, wo...)
# dagverwachting_df["dag_vd_week"] = pd.to_datetime(
#     dagverwachting_df["dag"], dayfirst=True
# ).dt.strftime("%a")

# # Session state voor dagindex
# if "dag_index" not in st.session_state:
#     st.session_state["dag_index"] = 0
    
# # Weertype icoontjes
# weer_icons = {
#     "zon": "☀️",
#     "halfbewolkt": "⛅",
#     "bewolkt": "☁️",
#     "regen": "🌧️",
#     "onweer": "⛈️",
#     "sneeuw": "❄️"
# }

# # Kleurthema afhankelijk van weer
# theme_colors = {
#     "zon": "linear-gradient(150deg, #FFD500, #F2F5F1)",
#     "halfbewolkt": "linear-gradient(135deg, #87CEEB, #FFFFFF)",
#     "bewolkt": "linear-gradient(135deg, #B0C4DE, #F0F0F0)",
#     "regen": "linear-gradient(135deg, #00BFFF, #F0F0F0)",
#     "onweer": "linear-gradient(135deg, #708090, #2F4F4F)",
#     "sneeuw": "linear-gradient(135deg, #E0FFFF, #FFFFFF)",
# }


# # Navigatieknoppen
# col1, col2, col3 = st.columns([1, 6, 1])
# with col1:
#     if st.button("◀️"):
#         if st.session_state["dag_index"] > 0:
#             st.session_state["dag_index"] -= 1
# with col3:
#     if st.button("▶️"):
#         if st.session_state["dag_index"] < len(dagverwachting_df) - 1:
#             st.session_state["dag_index"] += 1

# # Geselecteerde dag ophalen
# selected_day = dagverwachting_df.iloc[st.session_state["dag_index"]]
# icon = weer_icons.get(selected_day["image"], "🌤️")
# bg_color = theme_colors.get(selected_day["image"], "linear-gradient(135deg, #89CFF0, #FFFFFF)")

# # Weerkaartje (app-stijl)
# st.markdown(
#     f"""
#     <div style="padding:20px; border-radius:30px; background:{bg_color}; 
#                 box-shadow: 0px 4px 12px rgba(0,0,0,0.15); text-align:center; color:black;">
#         <h2 style="margin-bottom:10px;">{icon} Weer op {selected_day['dag_vd_week']} {selected_day['dag']}</h2>

        
#     <div style="padding:20px; border-radius:30px; background:{bg_color}; 
#                 box-shadow: 0px 4px 12px rgba(0,0,0,0.15); text-align:center; color:black;">
#         <p style="font-size:20px; margin:5px;">🌡️ <b>Max:</b> {selected_day['max_temp']}°C</p>
#         <p style="font-size:20px; margin:5px;">🌡️ <b>Min:</b> {selected_day['min_temp']}°C</p>
#         <p style="font-size:20px; margin:5px;">💨 <b>Wind:</b> {selected_day['windbft']} Bft ({selected_day['windkmh']} km/h, {selected_day['windr']})</p>
#         <p style="font-size:20px; margin:5px;">☔ <b>Kans op regen:</b> {selected_day['neersl_perc_dag']}%</p>
#         <p style="font-size:20px; margin:5px;">☀️ <b>Zonkans:</b> {selected_day['zond_perc_dag']}%</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Mooie select_slider onderaan
# weekdagen = dagverwachting_df["dag_vd_week"].tolist()
# chosen_day = st.select_slider(
#     "Kies een dag",
#     options=weekdagen,
#     value=weekdagen[st.session_state["dag_index"]],
#     label_visibility="collapsed"
# )

# # Synchroniseren met knoppen
# st.session_state["dag_index"] = weekdagen.index(chosen_day)

#%%


#%%


#%%



