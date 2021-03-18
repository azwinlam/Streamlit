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
    return pd.read_csv("temp_df.csv", index_col=0, header=0)

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
cuisine_array = df['cuisine_en'].unique()
cuisine_array = np.insert(cuisine_array, 0, values="All Cuisine")

pick_cuisine = st.sidebar.selectbox(
        'Pick Cuisine:', cuisine_array)

if pick_district == "All District" and pick_cuisine == "All Cuisine":
    df = df.iloc[:,:]
if pick_district == "All District" and pick_cuisine != "All Cuisine":
    df = df.loc[df.cuisine_en.str.contains(pick_cuisine)]
if pick_district != "All District" and pick_cuisine == "All Cuisine":
    df = df.loc[(df.district_en.str.contains(pick_district))]
if pick_district != "All District" and pick_cuisine != "All Cuisine":
    df = df.loc[(df.district_en.str.contains(pick_district)) & (df.cuisine_en.str.contains(pick_cuisine))]

st.header(f"There are {df.shape[0]} restaurants in {pick_district} for {pick_cuisine}")
st.write(df)