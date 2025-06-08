import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("🦠 COVID-19 Dashboard (Real Data)")
st.markdown("Visualizing COVID-19 cases, deaths, and tests by country over time.")

# Load dataset  
@st.cache_data
def load_data():
    df = pd.read_csv("covid_data.csv")

    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['Date'])
    
    # Select and rename columns
    df = df[['Country', 'Date', 'total_cases', 'total_deaths', 'total_tests']]
    
    df.rename(columns={
        'total_cases': 'Total Cases',
        'total_deaths': 'Total Deaths',
        'total_tests': 'Total Tests'
    }, inplace=True)

    return df

df = load_data()

# Sidebar filters
country = st.sidebar.selectbox("Select Country", df['Country'].unique())

# Convert datetime to date for the slider
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter data
filtered_df = df[
    (df['Country'] == country) &
    (df['Date'].dt.date >= date_range[0]) &
    (df['Date'].dt.date <= date_range[1])
]

# Show Metrics
st.subheader(f"📈 Stats for {country}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", f"{int(filtered_df['Total Cases'].max()):,}")
col2.metric("Total Deaths", f"{int(filtered_df['Total Deaths'].max()):,}")
if not filtered_df['Total Tests'].isnull().all():
    col3.metric("Total Tests", f"{int(filtered_df['Total Tests'].max()):,}")
else:
    col3.metric("Total Tests", "Data Not Available")

# Line chart
st.line_chart(filtered_df.set_index('Date')[['Total Cases', 'Total Deaths']])

# Data table
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)