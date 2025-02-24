import streamlit as st
import requests
import pickle
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler  # or any other relevant class from scikit-learn

# Load the transformer and model
with open('transformer.pkl', 'rb') as t_file:
    transformer = pickle.load(t_file)
with open('dtr.pkl', 'rb') as m_file:
    dtr = pickle.load(m_file)

# Function to get latitude & longitude for a given district, state, and country
def get_coordinates(district, state, country):
    query = f"{district}, {state}, {country}"
    geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}"

    response = requests.get(geocode_url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        data = response.json()
        if data:
            lat, lon = float(data[0]['lat']), float(data[0]['lon'])
            st.write(f"📍 Latitude: {lat}, Longitude: {lon}")  # Log in Streamlit
            return lat, lon
        else:
            st.error(f"Nominatim API returned an empty response for: {query}")
            st.json(response.json())  # Show full API response in Streamlit
            return None, None
    else:
        st.error(f"Error {response.status_code}: {response.text}")  # Show actual error
        return None, None

# Function to get average weather data for a year
def get_weather(district, state, country, year):
    lat, lon = get_coordinates(district, state, country)
    if lat is None or lon is None:
        return None, None  # Prevents app from breaking if location lookup fails

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=apparent_temperature,rain&start_date={year}-01-01&end_date={year}-12-31"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract hourly apparent temperature and rain data, filtering out None values
        temp_values = [t for t in data['hourly'].get('apparent_temperature', []) if t is not None]
        rainfall_values = [r for r in data['hourly'].get('rain', []) if r is not None]
        
        # Compute averages safely
        avg_temp = sum(temp_values) / len(temp_values) if temp_values else 0
        avg_rainfall = sum(rainfall_values) / len(rainfall_values) if rainfall_values else 0

        return avg_temp, avg_rainfall
    else:
        st.error("Failed to retrieve weather data. Please check the location.")
        return None, None

# Streamlit UI
st.title('Crop Yield Prediction App')

# Inputs from user
district = st.text_input('Enter District:')
state = st.text_input('Enter State:')
area = st.text_input('Enter Country (Area):')
item = st.text_input('Enter Crop Name (Item):')
pesticides = st.number_input('Enter Pesticides Used (tonnes):', min_value=0.0)
year = st.number_input('Enter Year:', min_value=2000, max_value=datetime.now().year, value=datetime.now().year)

if st.button('Predict Yield'):
    if district and state and area and item:
        avg_temp, avg_rainfall = get_weather(district, state, area, year)
        if avg_temp is not None:
            # Create DataFrame for prediction
            input_df = pd.DataFrame({
                'Year': [year],
                'average_rain_fall_mm_per_year': [avg_rainfall],
                'pesticides_tonnes': [pesticides],
                'avg_temp': [avg_temp],
                'District': [district],
                'State': [state],
                'Area': [area],  # Kept Area for model prediction
                'Item': [item]
            })
            
            input_transformed = transformer.transform(input_df)
            prediction = dtr.predict(input_transformed)
            st.success(f'Predicted Crop Yield: {prediction[0]:.2f} tonnes')
    else:
        st.error('Please enter District, State, Country (Area), and Item.')
