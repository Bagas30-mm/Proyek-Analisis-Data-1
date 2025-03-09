import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk memuat dataset
def load_dataset(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except FileNotFoundError:
        st.error(f"Error: File '{file_name}' tidak ditemukan.")
        return None

# Memuat dataset
bike_daily_data = load_dataset('day.csv')
bike_hourly_data = load_dataset('hour.csv')

# Konversi format tanggal
bike_daily_data['dteday'] = pd.to_datetime(bike_daily_data['dteday'])
bike_hourly_data['dteday'] = pd.to_datetime(bike_hourly_data['dteday'])

# Sidebar untuk filter
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", 
                                   [bike_daily_data['dteday'].min(), bike_daily_data['dteday'].max()])

# Filter data berdasarkan rentang tanggal
if len(date_range) == 2:
    bike_daily_data = bike_daily_data[(bike_daily_data['dteday'] >= pd.to_datetime(date_range[0])) &
                                      (bike_daily_data['dteday'] <= pd.to_datetime(date_range[1]))]
    bike_hourly_data = bike_hourly_data[(bike_hourly_data['dteday'] >= pd.to_datetime(date_range[0])) &
                                        (bike_hourly_data['dteday'] <= pd.to_datetime(date_range[1]))]

st.title("📊 Dashboard Penyewaan Sepeda")

# Visualisasi Pola Penyewaan Sepeda per Jam
st.subheader("Pola Penyewaan Sepeda per Jam")
hourly_rental_patterns = bike_hourly_data.groupby('hr')['cnt'].mean().reset_index()
fig_hourly = px.line(hourly_rental_patterns, x='hr', y='cnt', markers=True,
                     labels={'hr': 'Jam dalam Sehari', 'cnt': 'Rata-rata Penyewaan'},
                     title='Pola Penyewaan Sepeda per Jam')
st.plotly_chart(fig_hourly)

# Pola Penyewaan Hari Kerja vs Akhir Pekan
st.subheader("Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
day_type_rentals = bike_daily_data.groupby('workingday')['cnt'].mean().reset_index()
day_type_rentals['workingday'] = day_type_rentals['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})
fig_daytype = px.bar(day_type_rentals, x='workingday', y='cnt', color='workingday',
                      labels={'cnt': 'Rata-rata Penyewaan', 'workingday': 'Jenis Hari'},
                      title='Penyewaan Sepeda: Hari Kerja vs Akhir Pekan')
st.plotly_chart(fig_daytype)

# Korelasi Cuaca terhadap Penyewaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_rentals = bike_daily_data.groupby('weathersit')['cnt'].mean().reset_index()
weather_labels = {1: 'Cerah', 2: 'Mendung', 3: 'Hujan Ringan', 4: 'Hujan Lebat'}
weather_rentals['weathersit'] = weather_rentals['weathersit'].map(weather_labels)
fig_weather = px.bar(weather_rentals, x='weathersit', y='cnt', color='weathersit',
                     labels={'cnt': 'Rata-rata Penyewaan', 'weathersit': 'Kondisi Cuaca'},
                     title='Pengaruh Cuaca terhadap Penyewaan Sepeda')
st.plotly_chart(fig_weather)

# Kesimpulan
st.subheader("📌 Kesimpulan")
st.markdown("""
- **Puncak Penyewaan** terjadi pada jam sibuk: pagi (07:00-09:00) dan sore (17:00-19:00).
- **Penyewaan lebih tinggi pada hari kerja**, menunjukkan penggunaan sepeda sebagai moda transportasi utama.
- **Cuaca memengaruhi penyewaan**: kondisi cerah memiliki jumlah penyewaan tertinggi.
""")
