import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geopy import distance

st.set_page_config(
    page_title="Visualize Logbook",
    page_icon="ka.png",
    )
    
def load_css(file_name:str)->None:
    """
    Function to load and render a local stylesheet
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")


colors = {"A330": "#7D94CA", "A321": '#3F569D', "A320": '#1E3174'}
xlabel = 12
ylabel = 12
titlelabel = 14


st.title('Visualize Your Logbook')
st.header("By Azwin Lam")
st.header("")




@st.cache
def sample_csv():
    return pd.read_csv("mylogbook.csv",header=None, keep_default_na=False, nrows=8)

@st.cache
def sample_csv():
    return pd.read_csv("mylogbook.csv",header=None, keep_default_na=False, nrows=8)

@st.cache
def default_csv(allow_output_mutation=True):
    columns = ['date','flight_num','city_pair','ac_reg','block_time','off_block','airborne','landing','on_block','takeoff','land','autoland','commander']
    return pd.read_csv("loadsample.csv",names=columns, keep_default_na=False, skiprows=6)

@st.cache
def sample_csv2():
    return pd.read_csv("sample2.csv",header=None, keep_default_na=False, nrows=8)

sample_logbook = sample_csv()
sample_logbook2 = sample_csv2()

uploaded = False
loadsample = False

uploaded_file = st.file_uploader("Upload your Dragonair provided logbook as a comma-separated values (CSV) file")
st.text("Same format as the examples below (either is fine, 13 columns):")

if uploaded_file is None:
    if st.button('Load Demo'):
        df = default_csv().copy()
        st.write('Sample Loaded, Refresh the page to load your own CSV')
        uploaded_file = True
        loadsample = True

st.write(sample_logbook, nrows=10)
st.write(sample_logbook2)

if uploaded_file is not None:
    if loadsample == False:
        columns = ['date','flight_num','city_pair','ac_reg','block_time','off_block','airborne','landing','on_block','takeoff','land','autoland','commander']
        @st.cache
        def uploaded():
            return pd.read_csv(uploaded_file, names=columns)
        # Can be used wherever a "file-like" object is accepted:
        df = uploaded()
        count = 0
        for i in range(10):
            count += 1
            try:
                if df.iloc[i,:].values[0][0].isdigit():
                    break
            except:
                pass
        df = df.iloc[count-1:,:]
        df = df.reset_index(drop=True)

    #Df values modifications
    df['flight_num'] = df['flight_num'].astype(int)
    

    #Make split city pairs
    new = df['city_pair'].str.split(expand = True)
    df['origin'] = new[0]
    df['destination'] = new[1]
    df = df[['date',
 'flight_num',
 'city_pair',
 'origin',
 'destination',
 'ac_reg',
 'block_time',
 'off_block',
 'airborne',
 'landing',
 'on_block',
 'takeoff',
 'landing',
 'autoland',
 'commander']]
    #add AC Type into DF
    df["ac_type"] = 0
    df.loc[df['ac_reg'].str.contains("B-HS"),'ac_type'] = 'A320'
    df.loc[df['ac_reg'].str.contains("B-HT"),'ac_type'] = 'A321'
    df.loc[df['ac_reg'].str.contains("B-L"),'ac_type'] = 'A330'
    df.loc[df['ac_reg'].str.contains("B-HW"),'ac_type'] = 'A330'
    df.loc[df['ac_reg'].str.contains("B-HL"),'ac_type'] = 'A330'
    df.loc[df['ac_reg'].str.contains("B-HY"),'ac_type'] = 'A330'
    # change block times to date_time
    uploaded = True

if uploaded == True:
  
    st.write("Your Logbook Data:") 
    st.write(df)

    option = st.selectbox(
        'Show all flights with:',
        df['commander'].unique())
    sectors = df[df["commander"]== option].shape[0]
    st.subheader(f"You flew with {option} {sectors} times")
    st.write(df[df["commander"]== option])


    #Which route flown most
    top = 30
    top = st.slider('How many routes to show:',value =30, min_value=1, max_value=50, step=1)
    fig, ax = plt.subplots()
    ax = df['flight_num'].value_counts().head(top).plot(kind='bar',color= colors["A320"])
    
    ax.set_title("Routes Flown Most", fontsize=titlelabel)
    ax.set_xlabel("Routes No.", fontsize=xlabel);
    ax.set_ylabel("Sector Count", fontsize=ylabel);
    st.pyplot(fig)

    #Which aircraft type did i fly most?
    fig, ax = plt.subplots()
    ax = df['ac_type'].value_counts().plot(kind='barh', color = [colors["A321"],colors["A320"],colors["A330"]]);
    
    ax.set_title("Aircraft Type Flown Most", fontsize=titlelabel)
    ax.set_xlabel("Number of Sectors", fontsize=xlabel);
    ax.set_xticks(range(0,df.shape[0],200))
    st.pyplot(fig)

    #Which Pilot did I fly with most?
    top2 = st.slider('How many pilots to show:',value=10, min_value=1, max_value=50, step=1)
    
    fig, ax = plt.subplots()
    ax = df["commander"].value_counts(ascending=False).head(top2).plot(kind="barh",figsize=(10,7),color = colors["A320"])
    ax.invert_yaxis()
    ax.set_title("Most Flown Sectors", fontsize=titlelabel)
    ax.set_xlabel("Sectors", fontsize=xlabel)
    st.pyplot(fig)

    #Time Spent with Pilot
    df['block_time'] = pd.to_datetime(df['block_time'])
    df['block_time'] = df['block_time'].dt.strftime('%H:%M:%S')
    df['block_time'] = pd.to_timedelta(df['block_time'])
    top3 = st.slider('How many pilots to show:',value=20, min_value=1, max_value=30, step=1)
    fig, ax = plt.subplots()

    timespent = df.groupby('commander')['block_time'].sum()
    timespent = timespent.reset_index().set_index('commander')
    ax = timespent.block_time.astype('timedelta64[h]').sort_values(ascending=True)[-top3:].plot.barh(color = colors["A320"])
    ax.set_title(f"Cockpit Hours Shared, Top {top3} Pilots", fontsize=titlelabel)
    ax.set_xlabel("Hours", fontsize=xlabel)
    ax.set_ylabel("Commander", fontsize=ylabel)
    st.pyplot(fig)

    #Airframe
    import matplotlib.patches as mpatches
    fig, ax = plt.subplots()
    sort_graph = df.groupby(["ac_type","ac_reg"]).count()
    sort_graph = sort_graph.sort_values(by=["ac_type","date"],ascending=False).date
    # sort_graph.plot.bar(color= [colors[i] for i in sort_graph.index.get_level_values(0)],legend=False)
    ax = sort_graph.plot.bar(color=[colors[i] for i in sort_graph.index.get_level_values(0)])
    ax.set_title("Sectors On Each Airframe Sorted by Type and Registration")
    ax.set_ylabel("Count")
    ax.set_xlabel("Type and Registration")
    ax.set_xticklabels([i for i in sort_graph.index.get_level_values(1)],fontsize=8)

    a330_patch = mpatches.Patch(color="#7D94CA", label='A330')
    a321_patch = mpatches.Patch(color="#3F569D", label='A321')
    a320_patch = mpatches.Patch(color="#1E3174", label='A320')
    plt.legend(handles=[a330_patch,a321_patch,a320_patch],loc="best")

    st.pyplot(fig)


    #Sectors Not Hong Kong
    china_l = ['HKG','HGH','SYX','NGB','PVG','CSX','HAK','NKG','CGO','WNZ','XMN','FOC','CKG','CAN','XIY','WUH','CTU','PEK','TAO','KWL','KMG','SHA','TNA',"NNG","KMQ","MFM"]
    non_china_l = ['HKT','HAN','CRK','OKA','BKI','TPE', 'PNH','RMQ','KHH','FUK','CJU','CNX','RGN','DAD','MNL','CCU','REP','PUS','HND','HIJ','BLR','PEN','KIJ','DPS','KUL','DAC','KTM',"DVO","TKS","KMQ","KNO"]
    china_colors = {k:"#df2407" for k in china_l}
    non_china_colors = {k:"#22559E" for k in non_china_l}

    def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z

    port_colors =  merge_two_dicts(china_colors, non_china_colors)

    top4 = st.slider('How many destinations to show:',value=20, min_value=1, max_value=200, step=1)

    fig, ax = plt.subplots()
    dest_graph = df.destination.value_counts()[1:top4]
    ax = dest_graph.plot.bar(color=["black" if i not in port_colors else port_colors[i] for i in dest_graph.index])
    ax.set_title("Sectors To Each Destination (Not-HKG)")
    ax.set_ylabel("Count")
    ax.set_ylabel("Destinations")


    china_patch = mpatches.Patch(color="#df2407", label='China')
    non_china_patch = mpatches.Patch(color="#22559E", label='Non-China')

    plt.legend(handles=[china_patch,non_china_patch],loc="best")
    
    st.pyplot(fig)


    try:
        @st.cache
        def get_icao():
            
            return pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat", header=None, index_col=0)
        
        df_icao = get_icao()
        df_icao.columns = ['airport_name','city_name','country','IATA','ICAO','latitude','longtitude','a','b','c','region','d','e']
        ka_icao = pd.DataFrame(columns=['airport_name','city_name','country','IATA','ICAO','latitude','longtitude','a','b','c','region','d','e'])

        
        all_ports = df.origin.tolist() + df.destination.tolist()
        for i in set(all_ports):
            df2 = df_icao[df_icao["IATA"]==i]
            ka_icao = ka_icao.append(df2)
        temp_df = ka_icao[["IATA","latitude","longtitude"]]

        temp_list = temp_df.values.tolist()
        distance_d = {}
        for value in temp_list:
            distance_d[value[0]] = (value[1],value[2]) 

        def applydistance(origin,destination):
            try:
                origin = distance_d[origin]
                destination = distance_d[destination]
                return distance.distance(origin,destination).nm
            except:
                return 0
        
        
        df["distanceflown"] = np.arange(df.shape[0])
        

        df.distanceflown = df.distanceflown.apply(lambda x: round(applydistance(df.origin.values[x],df.destination.values[x])),0)

        @st.cache
        def get_total():
            return df.distanceflown.sum()

        total_distance_flown = get_total()
        st.subheader(f"You have flown a total of {total_distance_flown:,} nm in your career at Dragonair.")
        st.text("***Based on the ARPs great circle distance")
        st.write(df[["city_pair","distanceflown"]])
    except:
        pass

    st.header("")
    st.subheader('''If there are any bugs or new ideas for visualizations, please reach me on Linkedin at https://www.linkedin.com/in/azwinlam/''')