import streamlit as st
import pandas as pd
from models import fetch_flights_by_filters, add_flight, delete_flight
import numpy as np
import joblib

# Streamlit UI setup
st.set_page_config(layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Flight Delay Prediction", "Flight Management"])

# Shared Image
st.image("airplane.png", use_container_width=True)

# Load the saved model
@st.cache_resource
def load_model():
    return joblib.load("catboost-model-final.pkl")

# Load the label encoders
@st.cache_resource
def load_label_encoders():
    return joblib.load("cb_all_label_encoders.pkl")

# Load the origin city and airline mappings
@st.cache_resource
def load_mappings():
    origin_city_mapping = pd.read_csv("origin_city_mapping.csv").set_index("ORIGIN_CITY")["ORIGIN_CITY_ENCODED"].to_dict()
    dest_city_mapping = pd.read_csv("dest_city_mapping.csv").set_index("DEST_CITY")["DEST_CITY_ENCODED"].to_dict()
    airline_mapping = pd.read_csv("airline_mapping.csv").set_index("AIRLINE")["AIRLINE_ENCODED"].to_dict()
    return origin_city_mapping, dest_city_mapping, airline_mapping

# Initialize resources
model = load_model()
label_encoders = load_label_encoders()
origin_city_mapping, dest_city_mapping, airline_mapping = load_mappings()


# Define seasons based on month
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'
    
def safe_transform(encoder, value, placeholder=-1):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        # Add the placeholder to the classes
        encoder.classes_ = np.append(encoder.classes_, value)
        return placeholder


# Page 1: Flight Delay Prediction
if page == "Flight Delay Prediction":
    st.title("Flight Delay Prediction")

    # Input fields for prediction
    col1, col2 = st.columns(2)
    departure_city = col1.selectbox("Departure City", list(origin_city_mapping.keys()))
    arrival_city = col2.selectbox("Arrival City", list(dest_city_mapping.keys()))

    col3, col4 = st.columns(2)
    departure_date = col3.date_input("Departure Date")
    departure_time = col4.text_input("Departure Time (HHMM)")

    # Validate the time input
    if departure_time:
        if (
            not departure_time.isdigit()  # Ensure input is all digits
            or len(departure_time) != 4  # Ensure input is exactly 4 characters
            or not (0 <= int(departure_time[:2]) <= 23)  # Validate hour (HH) is 00-23
            or not (0 <= int(departure_time[2:]) <= 59)  # Validate minutes (MM) are 00-59
        ):
            st.error("Invalid time! Please enter a valid time in HHMM format (0000 to 2359).")

    col5, col6 = st.columns(2)
    airline = col5.selectbox("Select Airline", list(airline_mapping.keys()))
    flight_number = col6.text_input("Flight Number")

    # Prediction Button
    if st.button("Predict Delay"):
        if departure_city and arrival_city and departure_date and departure_time and airline and flight_number:


            selected_month = departure_date.month
            season = get_season(selected_month)

            # Encode inputs using label encoders
            departure_city_encoded = label_encoders["ORIGIN_CITY"].transform([departure_city])[0]
            arrival_city_encoded = label_encoders["DEST_CITY"].transform([arrival_city])[0]
            airline_encoded = label_encoders["AIRLINE"].transform([airline])[0]
            season_encoded = label_encoders["SEASON"].transform([season])[0]
            date_encoded = safe_transform(label_encoders["FL_DATE"], departure_date)
            time_encoded = safe_transform(label_encoders["CRS_DEP_TIME"], departure_time)

            # Prepare the input features
            features = np.array([[airline_encoded, season_encoded, departure_city_encoded, arrival_city_encoded, date_encoded, departure_time]])

            # Prediction
            prediction_proba = model.predict_proba(features)[0]
            
            prediction = model.predict(features)
            predicted_delay = prediction[0]
            # Display prediction result
            if predicted_delay == 1:
                st.success(f"The flight is expected to be **Delayed** with a probability of {prediction_proba[1]:.2%}")
            else:
                st.success(f"The flight is expected to be **On Time** with a probability of {prediction_proba[0]:.2%}")
        else:
            st.error("Please fill in all the fields to predict the delay.")

# Page 2: Flight Management
elif page == "Flight Management":
    st.title("Flight Management")

    # Search Flights
    st.header("Search Flights")
    input_fl_number = st.text_input("Enter Flight Number")
    input_fl_date = st.date_input("Select Flight Date")

    input_airline = st.selectbox("Select Airline", list(airline_mapping.keys()), key="airline_selectbox")

    if st.button("Search Flight"):
        if input_fl_number and input_fl_date and input_airline:
            filtered_flights = fetch_flights_by_filters(input_fl_number, input_fl_date, input_airline)
            if not filtered_flights.empty:
                st.dataframe(filtered_flights)
            else:
                st.warning("No flights found for the given criteria.")
        else:
            st.error("Please provide Flight Number, Flight Date, and Airline!")

    # Add a new flight
    st.header("Add New Flight")
    FL_DATE = st.date_input("Flight Date")
    AIRLINE = st.selectbox("Airline", list(airline_mapping.keys()))
    AIRLINE_CODE = st.text_input("Airline Code")
    FL_NUMBER = st.text_input("Flight Number")
    ORIGIN_CITY = st.selectbox("Departure City", list(origin_city_mapping.keys()))
    DEST_CITY = st.selectbox("Arrival City", list(dest_city_mapping.keys()))

    if st.button("Add Flight"):
        new_flight = (
            FL_DATE,
            AIRLINE,
            AIRLINE_CODE,
            FL_NUMBER,
            ORIGIN_CITY,
            DEST_CITY,
        )
        add_flight(new_flight)
        st.success("Flight added successfully!")

    # Delete a flight
    st.header("Delete Flight Data")
    delete_fl_number = st.text_input("Enter Flight Number to Delete", key="delete_fl_number")
    delete_fl_date = st.date_input("Select Flight Date to Delete", key="delete_fl_date")

    if st.button("Delete Flight"):
        if delete_fl_number and delete_fl_date:
            result = delete_flight(delete_fl_number, delete_fl_date)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(result["message"])
        else:
            st.error("Please provide Flight Number and Flight Date to delete!")
