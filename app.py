import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

@st.cache(suppress_st_warning=True)
def load_data():
    cols = ['Occurance', 'City', 'State', 'Country', 'Shape', 
            'Duration', 'Duration Original', 'Description', 
            'Last seen', 'Latitude', 'Longitude']
    df = pd.read_csv('ufo-scrubbed-geocoded-time-standardized.csv', 
                     header=None, names=cols)
    df = df.loc[df.Country == 'us']
    df.Occurance = df.Occurance.str.replace('24:00', '00:00')
    df.Occurance = pd.to_datetime(df.Occurance)
    df = df.loc[df.Longitude > -125]
    df = df.loc[df.Longitude < -67]
    #df = df[pd.to_numeric(df.Latitude, errors='coerce').notnull()]
    #df = df.loc[df.Latitude < 50]
    #df = df.loc[df.Latitude > 20]
    df['Year'] = df.Occurance.dt.year
    df = df.loc[df.Year >= 1947]
    df = df.loc[df.Year <= 2013]
    return df

df = load_data()

st.title('OMG, was that a UFO ?!')
st.markdown('by Paul-Louis Proeve')
'''
There have been more than 80,000 reports of strange objects in the sky
since 1947, according to The National UFO Reporting Center Online Database
(NUFORC). Whether you believe any of them were actual sightings of alien
activity is up to you.
'''

t1 = 'There has been a large increase in reportings especially in the 90s. While there were only '
t2 = ' reported sightings in '
t3 = ', in '
t4 = ' this number grew to '
t5 = '.'

vals = st.slider('', min_value=1947, max_value=2013, value=(1991, 1999))

num1 = len(df.loc[df.Year == vals[0]])
num2 = len(df.loc[df.Year == vals[1]])

st.write(t1, num1, t2, vals[0], t3, vals[1], t4, num2, t5)

f2 = px.histogram(df, x='Year', title='Number of UFO reportings in the US')
st.plotly_chart(f2, use_container_width=True)

'''
---

Many UFO sightings are said to be naturally occurring phenomena, such as
ball lightning or strange cloud formations, which have been mistakenly identified.
In the famous case of the Lubbock Lights in 1951, three science professors from
Texas Tech saw what appeared to be a semi-circle of lights in the sky. A US Air
Force investigation concluded the lights were birds reflecting the city’s new
street lights but later said it was a natural phenomenon. People have been using
a wide variety of descriptions for the shape of the sighting.
'''

f3 = px.histogram(df, x='Shape', title='Shape of the UFOs').update_xaxes(categoryorder='total descending')
st.plotly_chart(f3, use_container_width=True)

'''
---

NUFORC also collects the original description texts of the sightings.
Use the following chart to explore some of the reports.
'''

vals = st.slider(' ', min_value=1947, max_value=2013, value=(1991, 1999))
df_fil = df.loc[(df.Year >= vals[0]) & (df.Year <= vals[1])]
df_fil['txt'] = df.Description.str.contains('&#')
df_fil = df_fil[df_fil.txt == False]

f1 = px.scatter_geo(df_fil, lat='Latitude', lon='Longitude', hover_name='Description', title='Positions of reported occurances')
f1.update_geos(fitbounds="locations")
st.plotly_chart(f1, use_container_width=True)

st.markdown('---')
