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
    return pd.read_csv("temp_df2.csv", index_col=0, header=0)

st.title('Welcome to One Place Foodie')
st.header("By Trio")
st.header("")

df = default_csv()

pick_district = st.sidebar.selectbox(
        'Pick Location:',
        df['district_en'].unique())

pick_cuisine = st.sidebar.selectbox(
        'Pick Cuisine:',
        df['cuisine'].unique().sort())

df = df.loc[(df['district_en'] == pick_district) & (df['cuisine'] == pick_cuisine)]

st.write(df)