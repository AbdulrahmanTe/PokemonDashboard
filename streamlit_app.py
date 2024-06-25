import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import requests
import pprint

#https://pokemondashboard-8ux8z61yav3.streamlit.app/

st.set_page_config(page_title="First Stream Lit", page_icon="🔥")
st.title("Pokemon Dashboard")

pokemonNumber=st.slider("Select a number",min_value=1,max_value=1025,step=1)
#
url = f'https://pokeapi.co/api/v2/pokemon/{pokemonNumber}/'

#
response = requests.get(url)
pokemon = response.json()
print(response)

st.write(f"Pokemon Name: {pokemon['name']}")
st.write(f"Pokemon Image:")
st.image(pokemon['sprites']['front_default'])

st.write(f"Pokemon height: {pokemon['height']}")
st.write(f"Pokemon weight: {pokemon['weight']}")
st.write(f"Pokemon Type: {pokemon['types'][0]['type']['name']}")


moves = []
for x in pokemon['abilities']:
    moves.append(x['ability']['name'])

moves_df = pd.DataFrame(moves, columns=['Moves'])
moves_df.index = moves_df.index + 1

st.table(moves_df)

st.write(moves_df)

st.dataframe(moves_df)

SpecialStats = []
for x in pokemon['stats']:
    SpecialStats.append({'Special Stat Type': x['stat']['name'], 'Value': x['base_stat']})

stats_df = pd.DataFrame(SpecialStats)
stats_df.index = stats_df.index + 1

st.table(stats_df)

pokedex = pd.DataFrame(columns = ['name', 'height', 'weight', 'type','move_count'])

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemons = response.json()
        return pokemons['name'], pokemons['height'], pokemons['weight'],pokemons['types'][0]['type']['name'], len(pokemons['moves'])
    except:
        return 'Error', np.NAN, np.NAN, np.NAN,np.NAN

for poke_number in range(1, 50):
    pokedex.loc[poke_number] = get_details(poke_number)

st.write(pokedex)


result = pokedex.groupby('type').agg({'height': 'mean', 'weight': 'mean'}).reset_index()

result.columns = ['type', 'avg_height', 'avg_weight']


new_row = {'type': pokemon["name"], 'avg_height': pokemon["height"], 'avg_weight': pokemon["weight"]}
result=pd.concat([result,pd.DataFrame([new_row])], ignore_index=True)

#result.set_index('type', inplace=True)
st.write(result)

st.write("How does your pokemon's Height compare to other types of Pokemon?")
st.bar_chart(data=result, x='type', y='avg_height', x_label='Type', y_label='Average Height')

st.write("How does your pokemon's Weight compare to other types of Pokemon?")
st.bar_chart(data=result, x='type', y='avg_weight', x_label='Type', y_label='Average Weight')
