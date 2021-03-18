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

district_array = np.sort(df.district_en.unique())

all_district = []
for i in district_array:
    all_district.append(i)
show_all = " ".join(all_district)
district_array = np.insert(district_array, 0, values=show_all)

pick_district = st.sidebar.selectbox(
        'Pick Location:', district_array)

pick_cuisine = st.sidebar.selectbox(
        'Pick Cuisine:',
        df['cuisine'].unique())

df = df.loc[(df.district_en.str.contains(pick_district)) & (df['cuisine'] == pick_cuisine)]

st.write(df)