from key import API_KEY
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import re
import streamlit as st
import json

#FUNCTIONS
def reformat_with_join(number):
    num_str = str(int(number))
    formatted = '.'.join([num_str[:2], num_str[2:]])
    return float(formatted)

def request_data_location(location='Amsterdam', key=API_KEY):
    url_string = f'https://weerlive.nl/api/weerlive_api_v2.php?key={API_KEY}&locatie={location}'
    response = requests.get(url_string)
    json_data = response.json()
    live_weer_df = pd.DataFrame(json_data["liveweer"])
    return live_weer_df

#VARIABLES
url = 'https://www.webuildinternet.com/articles/2015-07-19-geojson-data-of-the-netherlands/townships.geojson'
geojson_data = requests.get(url).json()

pnamen = pd.read_csv('Plaatsnamen.csv',sep=';')
matches = pd.DataFrame(sorted([x['properties']['name'] for x in geojson_data['features']]))
pnamen = pnamen[np.isin(pnamen['Plaatsnaam'], matches)].reset_index(drop=True)

for i in range(len(pnamen)):
    pnamen['Longitude'][i], pnamen['Latitude'][i] = re.sub(r'[^\w\s]', '', pnamen['Longitude'][i]), re.sub(r'[^\w\s]', '', pnamen['Latitude'][i])
    pnamen['Latitude'][i] = reformat_with_join(pnamen['Latitude'][i])
    pnamen['Longitude'][i] = pnamen['Longitude'][i][0]+'.'+''.join(pnamen['Longitude'][i][1:])
    pnamen['Plaatsnaam'][i] = pnamen['Plaatsnaam'][i].replace("'",'')
pnamen[['Latitude','Longitude']] = pnamen[['Latitude','Longitude']].astype(float)
pnamen = pnamen.groupby('Provincie', as_index=False).head(4).reset_index(drop=True)

pnamen[['temp','gtemp','verw','samenv','windr']] = 0
for x in range(len(pnamen)):
    a= pnamen.loc[x,'Plaatsnaam']
    data = request_data_location(location=a)
    pnamen.at[x,'temp'] = data.temp
    pnamen.at[x,'gtemp'] = data.gtemp
    pnamen.at[x,'verw'] = data.verw
    pnamen.at[x,'samenv'] = data.samenv
    pnamen.at[x,'windr'] = data.windr

#MAP
# Dit plot gebruikt dorpen/steden die zowel in de geojson als in de KNMI plaatsnamenlijst terug kwamen, vandaar de gelimiteerde selectie
df = pnamen
#tering buttons werken niet kijk hier later naar idk man
button1 = dict(method= 'update',
               label='temp',
               args=[
                    {"z": [df['temp']]},
                    {"hover_name":'temp'},
                    {"coloraxis.colorscale": "redblue"}])
button2 = dict(method= 'update',
               label='gtemp',
               args=[
                    {"z": [df['gtemp']]},
                    {"hover_name":'gtemp'},
                    {"coloraxis.colorscale": "temps"}])



fig = px.choropleth_map(
    df,
    geojson=geojson_data,
    locations='Plaatsnaam',  
    featureidkey = 'properties.name',
    color='temp',
    color_continuous_scale='temps',
    title='Verdeling van API data onder Nederlandse dropen en steden',
    map_style="light",
    
)
fig.update_geos(fitbounds="locations", visible=True,resolution=50,)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0},
                  map={"zoom":5.8,
                  "center":{"lat": 52.092876, "lon": 5.104480}},
                  updatemenus=[dict(active=0,
                                    type='buttons',
                                    direction='right',
                                    buttons=[button1, button2],
                                    pad={"r": 10, "t": 10},
                                    showactive=True, 
                                    x=0.1,
                                    xanchor="left",
                                    y=1.1,
                                    yanchor="bottom")])

fig.show()
