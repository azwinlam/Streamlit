import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="One Place Foodie",
    )

@st.cache
def default_csv():
    return pd.read_csv("temp_df.csv", index_col=0, header=0)

st.title('Welcome to OPK')
st.header("By Trio")
st.header("")

df = default_csv()

pick_district = st.sidebar.selectbox(
        'Pick Location:',
        df['district_en'].unique())

df = df[df.district_en == pick_district]

st.write(df)