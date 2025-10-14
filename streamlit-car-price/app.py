import streamlit as st
import requests

API_URL = "https://car-price-api-v1.onrender.com/predict"

st.title("Car Price Predictor")

st.warning("⏳ First request may take 30-50 seconds (free tier cold start)")

# Dropdowns
manufacturer = st.selectbox(
    "Manufacturer",
    ["Toyota", "Honda", "BMW", "Ford", "Tesla"]
)

model = st.selectbox(
    "Model", 
    ["Corolla", "Civic", "3 Series", "F-150", "Model 3"]
)

fuel_type = st.selectbox(
    "Fuel Type",
    ["Petrol", "Diesel", "Electric", "Hybrid"]
)

# Number inputs
engine_size = st.number_input("Engine Size (L)", min_value=1.0, max_value=6.0, value=2.0, step=0.1)
year = st.number_input("Year of Manufacture", min_value=2010, max_value=2024, value=2020, step=1)
mileage = st.number_input("Mileage", min_value=0, max_value=200000, value=30000, step=1000)

# Predict button
if st.button("Predict Price"):
    payload = {
        "Manufacturer": manufacturer,
        "Model": model,
        "Fuel type": fuel_type,
        "Engine size": engine_size,
        "Year of manufacture": year,
        "Mileage": mileage
    }
    
    try:
        with st.spinner("Getting prediction..."):
            response = requests.post(API_URL, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            predicted_price = result.get("predicted_price_gbp")
            
            if predicted_price:
                st.success(f"## Predicted Price: ${predicted_price:,.2f}")
            else:
                st.error("No prediction returned")
                
    except requests.exceptions.Timeout:
        st.error("Request timed out. API may be waking up - try again in 10 seconds.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {str(e)}")
