import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import zipfile
import os

# Paths to the ZIP files
zip_file_path1 = 'athlete_events.csv.zip'
zip_file_path2 = 'noc_regions.csv.zip'

# Extract the ZIP files
with zipfile.ZipFile(zip_file_path1, 'r') as zip_ref:
    zip_ref.extractall()

with zipfile.ZipFile(zip_file_path2, 'r') as zip_ref:
    zip_ref.extractall()

# Load the CSV files from the extracted contents
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = helper.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')  # Ensure this image path is correct

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} overall performance")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")
    st.table(medal_tally)

elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.header("Country-wise Analysis")
    countries = df['region'].unique().tolist()
    selected_country = st.sidebar.selectbox("Select Country", countries)
    
    st.title(f"{selected_country} Performance")
    
    fig = plt.figure(figsize=(12, 5))
    plt.title("Medal Tally")
    ax = sns.heatmap(helper.country_event_heatmap(df, selected_country), annot=True, cmap="Blues")
    st.pyplot(fig)

    fig = plt.figure(figsize=(12, 5))
    plt.title("Year-wise Medal Tally")
    yearwise = helper.yearwise_medal_tally(df, selected_country)
    ax = sns.lineplot(data=yearwise, x='Year', y='Medal')
    st.pyplot(fig)

    most_successful = helper.most_successful_countrywise(df, selected_country)
    st.title(f"Most Successful Athletes from {selected_country}")
    st.table(most_successful)

elif user_menu == 'Athlete wise Analysis':
    st.sidebar.header("Athlete wise Analysis")
    sports = df['Sport'].unique().tolist()
    selected_sport = st.sidebar.selectbox("Select Sport", sports)

    st.title(f"Athletes' Performance in {selected_sport}")

    weight_height_df = helper.weight_v_height(df, selected_sport)
    fig = px.scatter(weight_height_df, x="Height", y="Weight", color="Medal", hover_name="Name", title="Height vs Weight of Athletes")
    st.plotly_chart(fig)

    st.title("Men vs Women Participation")
    gender_comparison = helper.men_vs_women(df)
    fig = px.line(gender_comparison, x="Year", y=["Male", "Female"], title="Male vs Female Athletes Over the Years")
    st.plotly_chart(fig)
