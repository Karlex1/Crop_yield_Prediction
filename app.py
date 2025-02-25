import streamlit as st
import requests
import pickle
import pandas as pd
from datetime import datetime, timedelta
import json

# Load transformer and model
try:
    with open('transformer.pkl', 'rb') as t_file:
        transformer = pickle.load(t_file)
    with open('dtr.pkl', 'rb') as m_file:
        dtr = pickle.load(m_file)
except Exception as e:
    st.error(f"Error loading model or transformer: {e}")

# Function to get latitude & longitude
def get_coordinates(district, state, country):
    query = f"{district}, {state}, {country}"
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        data = response.json()
        if data:
            lat, lon = float(data[0]['lat']), float(data[0]['lon'])
            return lat, lon
        else:
            st.error(f"Nominatim API returned an empty response for {query}")
            return None, None
    else:
        st.error(f"Geocoding API Error {response.status_code}: {response.text}")
        return None, None

# Function to convert prediction per bissa
def convert_to_total_yield(prediction_hg_per_ha, dimension):
    yield_per_bissa = (prediction_hg_per_ha * 0.1) / 74.25
    return yield_per_bissa * dimension  # Multiply by user-defined land size in bissa

# Function to get weather data
def get_weather(district, state, country, start_date):
    lat, lon = get_coordinates(district, state, country)
    if lat is None or lon is None:
        return None, None  

    # End date = current date + 16 days
    end_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

    # Extract the year from end_date
    year = int(end_date[:4])

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=apparent_temperature,rain&start_date={start_date}&end_date={end_date}"
    
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            if "hourly" not in data:
                st.error("Weather API response is missing 'hourly' data.")
                st.json(data)  # Debug response
                return None, None, year

            temp_values = [t for t in data['hourly'].get('apparent_temperature', []) if t is not None]
            rainfall_values = [r for r in data['hourly'].get('rain', []) if r is not None]

            avg_temp = sum(temp_values) / len(temp_values) if temp_values else 0
            avg_rainfall = sum(rainfall_values) / len(rainfall_values) if rainfall_values else 0

            return avg_temp, avg_rainfall, year
        except json.JSONDecodeError as e:
            st.error(f"Weather API JSON decode error: {e}")
            return None, None, year
    else:
        st.error(f"Weather API Error {response.status_code}: {response.text}")
        return None, None, None

# Streamlit UI
st.title('Crop Yield Prediction App')

district = st.text_input('Enter District:')
state = st.text_input('Enter State:')
area = st.text_input('Enter Country (Area):')
item = st.text_input('Enter Crop Name (Item):')

# Ask user for pesticides in KG and convert to tonnes
pesticides_kg = st.number_input('Enter Pesticides Used (kg):', min_value=0.0)
pesticides_tonnes = pesticides_kg / 1000  # Convert to tonnes

# Ask user for land size in bissa
dimension = st.number_input('Enter total land area in Bissa:', min_value=0.1)

# Ask user for start date
start_date = st.date_input("Select the planting/start date:", min_value=datetime(2000, 1, 1), max_value=datetime.now())

if st.button('Predict Yield'):
    if district and state and area and item:
        avg_temp, avg_rainfall, year = get_weather(district, state, area, start_date.strftime('%Y-%m-%d'))

        if avg_temp is not None and year is not None:
            # Construct DataFrame for prediction
            input_df = pd.DataFrame({
                'Year': [year],  # Add the extracted year
                'average_rain_fall_mm_per_year': [avg_rainfall],
                'pesticides_tonnes': [pesticides_tonnes],  # Use converted value
                'avg_temp': [avg_temp],
                'District': [district],
                'State': [state],
                'Area': [area],
                'Item': [item]
            })

            try:
                input_transformed = transformer.transform(input_df)

                prediction = dtr.predict(input_transformed)
                total_yield = convert_to_total_yield(prediction[0], dimension)

                st.success(f'Predicted Total Crop Yield: {total_yield:.2f} kg')

            except Exception as e:
                st.error(f"Prediction error: {e}")
    else:
        st.error('Please enter District, State, Country (Area), and Item.')
