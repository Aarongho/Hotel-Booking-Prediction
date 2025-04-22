import pickle
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import OneHotEncoder

# Load pre-trained model, encoder, and scaler
with open('xgb_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('encoder.pkl', 'rb') as file:
    encoder = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Streamlit UI configuration
st.set_page_config(page_title="Prediction Cancelling Hotel", page_icon="🏨", layout="centered")
st.markdown("<h1 style='text-align: center;'>Prediction On Cancelling Booking Hotel 🏨</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv("Dataset_B_hotel.csv")

df = load_data()

st.markdown("<h4 style='text-align: center;'>Here's an example of the Raw Hotel Dataset that is given in the question!</h4>", unsafe_allow_html=True)
with st.expander("📂 Raw Data "):
    st.dataframe(df.head(10))

# User input form for prediction
st.markdown("<h4 style='text-align: center;'>Input The Data you want to predict 🔮!</h4>", unsafe_allow_html=True)
with st.form("booking_form"):
    st.subheader("📋 Informasi Pemesanan")
    
    col1, col2 = st.columns(2)
    with col1:
        no_of_adults = st.number_input("👨‍👩‍👧‍👦 Jumlah Dewasa", min_value=0, value=2)
        no_of_children = st.number_input("🧒 Jumlah Anak", min_value=0, value=0)
        no_of_weekend_nights = st.number_input("🌙 Malam Akhir Pekan", min_value=0, value=1)
        no_of_week_nights = st.number_input("📆 Malam Hari Kerja", min_value=0, value=2)
        meal_plan_choice = st.selectbox("🍽️ Meal Plan", ["No Meal", "Meal Type 1", "Meal Type 2", "Meal Type 3"])
        required_car_parking_space = st.selectbox("🚗 Butuh Parkir?", options=[0, 1], format_func=lambda x: "Ya" if x else "Tidak")
        room_type_choice = st.selectbox("🛏️ Tipe Kamar", ["Tipe 1 ", "Tipe 2 ", "Tipe 3 ", "Tipe 4 ", "Tipe 5 ", "Tipe 6 ", "Tipe 7 "])
        lead_time = st.number_input("⏳ Lead Time (hari sebelum check-in)", min_value=0, value=30)

    with col2:
        arrival_year = st.number_input("📅 Tahun Kedatangan", min_value=2020, value=2024)
        arrival_month = st.slider("🗓️ Bulan Kedatangan", 1, 12, 5)
        arrival_date = st.slider("📆 Tanggal Kedatangan", 1, 31, 15)
        market_choice = st.selectbox("🧭 Segmentasi Pasar", ["Online", "Offline", "Agen Perjalanan", "Perusahaan", "Langganan", "Lainnya"])
        repeated_guest = st.selectbox("🔁 Tamu Berulang?", options=[0, 1], format_func=lambda x: "Ya" if x else "Tidak")
        no_of_previous_cancellations = st.number_input("❌ Cancel Sebelumnya", min_value=0, value=0)
        no_of_previous_bookings_not_canceled = st.number_input("✅ Booking Berhasil Sebelumnya", min_value=0, value=1)
        avg_price_per_room = st.number_input("💸 Harga Rata-Rata Kamar", min_value=0.0, value=100.0)
        no_of_special_requests = st.number_input("📝 Jumlah Request Khusus", min_value=0, value=0)

    st.markdown("")
    submit = st.form_submit_button("🔮 Prediksi Sekarang")

if submit:
    with st.spinner("⏳ Sedang memproses prediksi..."):
        input_data = pd.DataFrame([[
            no_of_adults, no_of_children, no_of_weekend_nights,
            no_of_week_nights, meal_plan_choice, required_car_parking_space,
            room_type_choice, lead_time, arrival_year, arrival_month,
            arrival_date, market_choice, repeated_guest,
            no_of_previous_cancellations, no_of_previous_bookings_not_canceled,
            avg_price_per_room, no_of_special_requests
        ]], columns=[
            'no_of_adults', 'no_of_children', 'no_of_weekend_nights',
            'no_of_week_nights', 'meal_plan_choice', 'required_car_parking_space',
            'room_type_choice', 'lead_time', 'arrival_year', 'arrival_month',
            'arrival_date', 'market_choice', 'repeated_guest',
            'no_of_previous_cancellations', 'no_of_previous_bookings_not_canceled',
            'avg_price_per_room', 'no_of_special_requests'
        ])

        #


