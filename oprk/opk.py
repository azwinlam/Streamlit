import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="One Place Foodie!",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache
def default_csv():
    return pd.read_csv("temp_df3.csv", index_col=0, header=0)

st.title('Welcome to One Place Foodie!v3')
st.header("By Trio")
st.header("")

df = default_csv()

#District Side Bar
district_array = np.sort(df.district_en.unique())
district_array = np.insert(district_array, 0, values="All District")

pick_district = st.sidebar.selectbox(
        'Pick Location:', district_array)


#Cuisine Side Bar
cuisine_array = df['cuisine'].unique()
cuisine_array = np.insert(cuisine_array, 0, values="All Cuisine")

pick_cuisine = st.sidebar.selectbox(
        'Pick Cuisine:',
        df['cuisine'].unique())

if pick_district == "All Cuisine" and pick_cuisine == "All Cuisine":
    df = df
if pick_district == "All District":
    df = df.loc[df['cuisine'] == pick_cuisine]
else:
    df = df.loc[(df.district_en.str.contains(pick_district)) & (df['cuisine'] == pick_cuisine)]

st.write(df)