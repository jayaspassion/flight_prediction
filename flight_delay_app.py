import streamlit as st
import mysql.connector
import pandas as pd

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
# col6.text_input("Input Field 6")

# Connect to the database
# @st.cache_resource
def get_db_connection():
    return mysql.connector.connect(
    host="flight-database.c9kakyqtso3n.us-east-1.rds.amazonaws.com",
    user="admin",
    password="flightpredictor999",
    database="flight_db"
)

# Fetch flights by filters
def fetch_flights_by_filters(flight_number, flight_date, airline):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM flight_data
    WHERE FL_NUMBER = %s AND FL_DATE = %s AND AIRLINE = %s
    """
    cursor.execute(query, (flight_number, flight_date, airline))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(results)

# Insert a new flight
def add_flight(flight):
    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO flight_data (FL_DATE, AIRLINE, AIRLINE_CODE, FL_NUMBER,
                            ORIGIN_CITY, DEST_CITY)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, flight)
    connection.commit()
    cursor.close()
    connection.close()

# Fetch distinct airline options
def fetch_airline_options():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT AIRLINE FROM flight_data ORDER BY AIRLINE")
    airlines = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return airlines

# Streamlit UI
st.title("Flight Management")

# Fetch flights by filters
st.header("Search Flights")
input_fl_number = st.text_input("Enter Flight Number")
input_fl_date = st.date_input("Select Flight Date")
# Fetch airline options for dropdown
airlines = fetch_airline_options()
selected_airline = st.selectbox("Select Airline", options=airlines)

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


