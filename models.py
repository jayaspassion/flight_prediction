from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date, select, and_, insert, delete
from sqlalchemy.sql import text  
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import streamlit as st

# Get the Database URL from Streamlit secrets
DATABASE_URL = st.secrets["DATABASE_URL"]

# Create the engine
engine = create_engine(DATABASE_URL)

# Metadata and Table definition
metadata = MetaData()
flight_data = Table(
    "flight_data", metadata,
    Column("FL_DATE", Date),
    Column("AIRLINE", String(255)),
    Column("AIRLINE_CODE", String(10)),
    Column("FL_NUMBER", String(255)),
    Column("ORIGIN_CITY", String(255)),
    Column("DEST_CITY", String(255)),
)

# Fetch flights by filters
def fetch_flights_by_filters(flight_number, flight_date, airline):
    try:
        with engine.connect() as connection:
            query = select(flight_data.c).where(
                and_(
                    flight_data.c.FL_NUMBER == flight_number,
                    flight_data.c.FL_DATE == flight_date,
                    flight_data.c.AIRLINE == airline
                )
            )
            result = connection.execute(query)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return pd.DataFrame()

# Insert a new flight
def add_flight(flight):
    try:
        with engine.connect() as connection:
            # Begin a transaction
            transaction = connection.begin()
            query = insert(flight_data).values(
                FL_DATE=flight[0],
                AIRLINE=flight[1],
                AIRLINE_CODE=flight[2],
                FL_NUMBER=flight[3],
                ORIGIN_CITY=flight[4],
                DEST_CITY=flight[5]
            )
            connection.execute(query)
            transaction.commit()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")


# **Delete a flight by FL_NUMBER and FL_DATE**
def delete_flight(flight_number, flight_date):
    try:
        with engine.connect() as connection:
            # Begin a transaction
            transaction = connection.begin()
            query = delete(flight_data).where(
                and_(
                    flight_data.c.FL_NUMBER == flight_number,
                    flight_data.c.FL_DATE == flight_date
                )
            )
            result = connection.execute(query)
            transaction.commit()
            if result.rowcount > 0:
                print(f"Deleted {result.rowcount} flight(s) successfully.")
                return {"message": "Flight deleted successfully"}
            else:
                print("No flight found for the given criteria.")
                return {"message": "No flight found"}
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return {"error": str(e)}        

def fetch_airline_mappings():
    try:
        with engine.connect() as connection:
            query = text("SELECT AIRLINE, AIRLINE_ENCODED FROM airline_mapping")
            result = connection.execute(query)
            return {row[0]: row[1] for row in result}
    except SQLAlchemyError as e:
        print(f"Database error: {e}. Falling back to CSV.")
        # Fallback to CSV
        try:
            df = pd.read_csv("airline_mapping.csv")
            return dict(zip(df["AIRLINE"], df["AIRLINE_ENCODED"]))
        except FileNotFoundError:
            print("Fallback CSV file not found.")
            return {}
        
def fetch_origin_city_mappings():
    try:
        with engine.connect() as connection:
            query = text("SELECT ORIGIN_CITY, ORIGIN_CITY_ENCODED FROM origin_city_mapping")
            result = connection.execute(query)
            return {row[0]: row[1] for row in result}
    except SQLAlchemyError as e:
        print(f"Database error: {e}. Falling back to CSV.")
        # Fallback to CSV
        try:
            df = pd.read_csv("origin_city_mapping.csv")
            return dict(zip(df["ORIGIN_CITY"], df["ORIGIN_CITY_ENCODED"]))
        except FileNotFoundError:
            print("Fallback CSV file not found.")
            return {}

def fetch_dest_city_mappings():
    try:
        with engine.connect() as connection:
            query = text("SELECT DEST_CITY, DEST_CITY_ENCODED FROM dest_city_mapping")
            result = connection.execute(query)
            return {row[0]: row[1] for row in result}
    except SQLAlchemyError as e:
        print(f"Database error: {e}. Falling back to CSV.")
        # Fallback to CSV
        try:
            df = pd.read_csv("dest_city_mapping.csv")
            return dict(zip(df["DEST_CITY"], df["DEST_CITY_ENCODED"]))
        except FileNotFoundError:
            print("Fallback CSV file not found.")
            return {}                
