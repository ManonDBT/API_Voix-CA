import streamlit as st

import matplotlib

import pandas as pd
import numpy as np
import re

st.title("Dashboard portail Voix-CA")
st.write("""Exploration de la base de donnée""")

df = pd.read_excel("/Users/manon/Projet/IA_Processing/labels-voix-ca-lot-6-reduit.xlsx")

def load_data(nrows):
    dfs = pd.read_excel("/Users/manon/Projet/IA_Processing/labels-voix-ca-lot-6-reduit-th.xlsx",nrows=nrows)
    dfs['date'] = pd.to_datetime(dfs['date'])
    return dfs


data_load_state = st.text('Chargement en cours...')
data = load_data(10000)
st.dataframe(data)
data_load_state.text('Chargement terminé!')



st.subheader('Nombre de compte rendu par jour')
data['date'].value_counts().plot.bar()
st.pyplot()


'''st.subheader('Nombre de thématiques')
df.groupby('category').text.count().plot.bar(ylim=0)\
.set(title="Représentation du nombre de thématiques",
xlabel="Thématiques", ylabel="Nombre de thématiques")
st.pyplot()'''


