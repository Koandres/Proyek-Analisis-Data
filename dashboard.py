import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "cnt": "total rental"
    }, inplace=True)
    
    return daily_orders_df

def create_byworkday_df(df):
    byworkday_df = day_df.groupby(by="workingday").cnt.sum().reset_index()
    byworkday_df.rename(columns={
        "cnt": "Total Rental"
    }, inplace=True)
    
    return byworkday_df

def create_byseason_df(df):
    byseason_df = day_df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "Total Rental"
    }, inplace=True)
    byseason_df['season'] = pd.Categorical(byseason_df['season'], ["spring", "summer", "fall", "winter"])
    
    return byseason_df

def create_byweather_df(df):
    byweather_df = day_df.groupby(by="weathersit").cnt.sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "Total Rental"
    }, inplace=True)
    byweather_df['weathersit'] = pd.Categorical(byweather_df['weathersit'], ["cerah", "berawan", "mendung", "ekstrem"])
    
    return byweather_df

day_df = pd.read_csv("day_data_changed.csv")
 
day_df.dteday = pd.to_datetime(day_df.dteday)

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/premium-vector/red-bike-rental-logo-with-map-pin-concept-biking-bycicle-sale-rent-bike-trip-company-mark-repair-isolated-white-background-flat-style-trend-modern-logotype-design-vector-illustration_117142-390.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
byworkday_df = create_byworkday_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)

st.header('Bike Sharing :sparkles:')

st.subheader('Daily Rentals')
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["total rental"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Perbandingan Jumlah Rental antara Hari Kerja dan Hari Libur")
   
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
  y="Total Rental", 
  x="workingday",
  data=byworkday_df.sort_values(by="Total Rental", ascending=False),
  palette=colors,
  ax=ax
)
ax.set_title("Total Bike Rental Count by workingday", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Kondisi Cuaca dan Musim")
   
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
  y="Total Rental", 
  x="season",
  data=byseason_df.sort_values(by="Total Rental", ascending=False),
  palette=colors,
  ax=ax
)
ax.set_title("Total Bike Rental Count by Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
 

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="Total Rental", 
    y="weathersit",
    data=byweather_df.sort_values(by="Total Rental", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Total Bike Rental Count by Weather", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
 
st.caption('Copyright (c) Dicoding 2023')
