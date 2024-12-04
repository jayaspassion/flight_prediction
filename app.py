import streamlit as st
import pandas as pd
from models import fetch_flights_by_filters, add_flight, delete_flight

# Streamlit UI setup
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Range")
range_value = st.sidebar.slider("Max Delay (mins)", min_value=0, max_value=100, value=50)

st.image("airplane.png", use_container_width=True)

# Grid layout
col1, col2 = st.columns(2)
col1.text_input("Departure Airport")
col2.text_input("Arrival Airport")

col3, col4 = st.columns(2)
col3.text_input("Departure Date")
col4.text_input("Departure Time")

col5, col6 = st.columns(2)
col5.text_input("Airlines")

# Streamlit UI
st.title("Flight Management")

# Fetch flights by filters
st.header("Search Flights")
input_fl_number = st.text_input("Enter Flight Number")
input_fl_date = st.date_input("Select Flight Date")
airline_options = ["Delta Air Lines Inc.", "United Air Lines Inc.", "American Airlines Inc.", "Southwest Airlines Co.", "JetBlue Airways", "Alaska Airlines Inc."]
selected_airline = st.selectbox("Select Airline", options=airline_options)

if st.button("Search Flight"):
    if input_fl_number and input_fl_date and selected_airline:
        filtered_flights = fetch_flights_by_filters(input_fl_number, input_fl_date, selected_airline)
        if not filtered_flights.empty:
            st.dataframe(filtered_flights)
        else:
            st.warning("No flights found for the given criteria.")
    else:
        st.error("Please provide Flight Number, Flight Date, and Airline!")

# Add a new flight
st.header("Add New Flight")
FL_DATE = st.date_input("Flight Date")
AIRLINE = st.text_input("Airline")
AIRLINE_CODE = st.text_input("Airline Code")
FL_NUMBER = st.text_input("Flight Number")
ORIGIN_CITY = st.text_input("Origin City")
DEST_CITY = st.text_input("Destination City")

if st.button("Add Flight"):
    new_flight = (
        FL_DATE, AIRLINE, AIRLINE_CODE, FL_NUMBER, ORIGIN_CITY, DEST_CITY
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
