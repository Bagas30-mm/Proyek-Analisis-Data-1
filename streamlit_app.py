import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your datasets
bike_daily_data = pd.read_csv('/content/day.csv')
bike_hourly_data = pd.read_csv('/content/hour.csv')

# --- Title and Introduction ---
st.title("Dashboard Analisis Data Bike Sharing")
st.markdown("**Deskripsi:** Dashboard ini menampilkan hasil analisis data penyewaan sepeda.")

# --- Sidebar ---
st.sidebar.header("Filter Data")
selected_data = st.sidebar.selectbox("Pilih Dataset", ["Data Harian", "Data Per Jam"])

# --- Data Display and Visualization ---
if selected_data == "Data Harian":
    st.subheader("Data Harian")
    st.dataframe(bike_daily_data.head())  # Display a portion of the data
    # Add visualizations for daily data here (e.g., line chart, bar chart)
else:
    st.subheader("Data Per Jam")
    st.dataframe(bike_hourly_data.head())
    # Add visualizations for hourly data here (e.g., scatter plot, heatmap)

# --- Analysis and Insights ---
st.header("Analisis dan Insight")
# Add your analysis and insights here, using Markdown or other components

# ... (Add more visualizations and analysis sections as needed) ...
