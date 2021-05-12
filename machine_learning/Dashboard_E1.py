import streamlit as st

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import re

st.title("Tableau de bord portail Voix-CA")
st.write("""Exploration de la base de donnée""")

df = pd.read_excel("/Users/manon/Projet/IA_Processing/labels-voix-ca-lot-6-reduit.xlsx")

def load_data(nrows):
    dfs = pd.read_excel("/Users/manon/Projet/IA_Processing/labels-voix-ca-lot-6-reduit-th.xlsx",nrows=nrows)
    dfs['date'] = pd.to_datetime(dfs['date'])
    dfs['year'] = dfs['date'].dt.year
    dfs['month'] = dfs['date'].dt.month
    dfs['day'] = dfs['date'].dt.day
    dfs = dfs.set_index(['date'])
    return dfs


data_load_state = st.text('Chargement en cours...')
data = load_data(10000)
st.dataframe(data)
data_load_state.text('Chargement terminé!')


st.subheader('Nombre de comptes rendus par Caisse Régionale sur l\'année 2020')
plt.rcdefaults()
fig, ax = plt.subplots()
# Example data
df_2020 = data.loc['2020']
CR = ('Centre-France', 'Languedoc', 'Brie Picardie')
y_pos = np.arange(len(CR))
performance = df_2020['CR'].value_counts()
ax.barh(y_pos, performance, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(CR)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Nombre de comptes rendus')
st.pyplot(fig)


st.subheader('Evolution du nombre de comptes rendus à l\'année par Caisses Régionales ')
labels = ['2019', '2020']
centre_france = [206, 542]
languedoc = [92, 406]
brie_picardie = [97, 261]
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars
fig3, ax = plt.subplots()
rects1 = ax.bar(x - width/3, centre_france, width, label='Centre-France')
rects2 = ax.bar(x , languedoc, width, label='Languedoc')
rects3 = ax.bar(x + width/3, brie_picardie, width, label='Brie-Picardie')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Nombre de comptes rendus')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
fig3.tight_layout()
st.pyplot(fig3)



fig2, ax = plt.subplots()
st.subheader('Représentation du nombre de thématiques sur l\'ensemble des années' )
df.groupby('category').text.count().plot.bar(ylim=0)\
.set(title=" ",
xlabel="Thématiques", ylabel="Nombre de thématiques")
st.pyplot(fig2)

st.set_option('deprecation.showPyplotGlobalUse', False)
