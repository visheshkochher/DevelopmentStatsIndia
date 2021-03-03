import pandas as pd
import streamlit as st
import plotly.express as px


# Load Data
data = pd.read_excel('src/Koch_NFHS4_Resource Planning.xlsx', sheet_name='Sheet1', header=1)

# GET DIMENSIONS AND MEASURES
state_district_dict = {k: data[data['statname'] == k]['District Name'].unique() for k in data.statname.unique()}
kpi_list = data.columns[4:]

# SET STREAMLIT LAYOUT
st.set_page_config(layout='wide')
st.header("""DISTRICT-WISE DATA EXPLORE""")
x = st.beta_container()
x.write('')
side_col, content_col = st.beta_columns([1,3])

# MAKE SIDE BAR FOR SELECTIONS
with side_col:
    state_selected = st.selectbox("Select State",
                                  [x for x in state_district_dict.keys()])
    district_selected = st.selectbox("Select District",
                                     ['All']+list(state_district_dict[state_selected]))

    kpi1_selected = st.selectbox("Select Primary Indicator",
                                 ['All'] if district_selected != 'All' else kpi_list)

    kpi2_selected = st.selectbox("Select Primary Indicator",
                                 [''] if district_selected != 'All' else [x for x in kpi_list if x != kpi1_selected])


# CALCULATE RESULT
# Filter Data and Vizualize
if district_selected == 'All':
    filtered_data = data.loc[(data['statname'] == state_selected)]#[[kpi1_selected, kpi2_selected]]
    fig = px.bar(filtered_data,
                 x='District Name',
                 y=[kpi1_selected, kpi2_selected],
                 barmode='group')
else:
    filtered_data = data.loc[(data['statname']==state_selected) &
                     (data['District Name']==district_selected)]
    fig = px.bar(filtered_data,
                 x='District Name',
                 y=kpi_list[:10],
                 barmode='group')

# DISPLAY RESULT
with content_col:
    st.text('Data Deep Dive')
    st.dataframe(filtered_data)
    st.plotly_chart(fig, use_container_width=True)

