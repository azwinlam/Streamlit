import streamlit as st
import pandas as pd

@st.cache
def default_csv():
    return pd.read_csv("temp_df.csv", header=0)

st.title('Welcome to OPK')
st.header("By Trio")
st.header("")

df = default_csv()

st.write(df)