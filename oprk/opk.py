import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import pydeck as pdk

token = "pk.eyJ1IjoiYXp3aW5sYW0iLCJhIjoiY2ttZWZ1OXlmMGhneTJvbnpmbjN0cGlncCJ9.F9dG4cOF6weMIwUx1ajL6A"

st.set_page_config(
    page_title="One Place Foodie!",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache
def default_csv():
    return pd.read_csv("temp_df4.csv", index_col=0, header=0)

st.title('Welcome to One Place Foodie!v3')
st.header("By Trio")
st.header("")

df = default_csv()

#District Side Bar
district_array = np.sort(df.district_en.unique())
district_array = np.insert(district_array, 0, values="All District")

pick_district = st.sidebar.selectbox(
        'Pick Location:', district_array, index=4)


#Cuisine Side Bar
cuisine_array = df['cuisine_en'].unique()
cuisine_array = np.insert(cuisine_array, 0, values="All Cuisine")

pick_cuisine = st.sidebar.selectbox(
        'Pick Cuisine:', cuisine_array)

if pick_district == "All District" and pick_cuisine == "All Cuisine":
    df_temp = df.iloc[:,:]
if pick_district == "All District" and pick_cuisine != "All Cuisine":
    df_temp = df.loc[df.cuisine_en.str.contains(pick_cuisine)]
if pick_district != "All District" and pick_cuisine == "All Cuisine":
    df_temp = df.loc[(df.district_en.str.contains(pick_district))]
if pick_district != "All District" and pick_cuisine != "All Cuisine":
    df_temp = df.loc[(df.district_en.str.contains(pick_district)) & (df.cuisine_en.str.contains(pick_cuisine))]

st.header(f"There are {df.shape[0]} restaurants in {pick_district} for {pick_cuisine}")
st.write(df_temp)

rest_num = st.number_input(label="Input Restaurant Number",value=int(df_temp.index[0][4:]),step = 1)

restaurant = df[df.index==f"rest{rest_num}"]

price_d = {50: "Less than 50 HKD",
            51: "51-100 HKD", 
            101: "101-200 HKD", 
            201: "201-400 HKD", 
            401: "401-800 HKD", 
            801: "More than 801 HKD"}

#Address Lat Lon lookup
url = "https://www.als.ogcio.gov.hk/lookup?q="
headers = {"Accept": 'application/json', "Accept-Language": 'en'}
address = restaurant.add_en.values[0]
res = requests.get(url+address, headers=headers)

geo = json.loads(res.text)
lat = float(geo["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Latitude"])
lon = float(geo["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Longitude"])
geo_address = pd.DataFrame({"lat":[lat], "lon":[lon]}, index=None)

st.write(f"Restraunt Name: {restaurant.name.values[0]}, {restaurant.name2.values[0]} ")
st.write(f"Cuisine: {restaurant.cuisine_en.values[0]}")
st.write(f"District: {restaurant.district_en.values[0]}")
st.write(f"Address: {restaurant.add_en.values[0]}")
st.write(f"Price: {price_d[restaurant.price.values[0]]}")

st.map(geo_address,zoom=16)
st.write(lat,lon)

# st.pydeck_chart(pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=pdk.ViewState(
#         latitude=lat,
#         longitude=lon,
#         zoom=16,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#             'HexagonLayer',
#             data=geo_address,
#             elevation_scale=4,
#             get_position="[lon,lat]",
#             radius=10,
#         ),
#         pdk.Layer(
#             "ScatterplotLayer",
#             data=geo_address,
#             get_position='[lon,lat]',
#             get_color='[200,30,0,160]',
#             get_radius=200
#         ),
#     ],
# ))