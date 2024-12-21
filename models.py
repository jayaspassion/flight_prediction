from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Date, select, and_, insert, delete, update
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
    Column("FL_NUMBER", String(255)),
    Column("ORIGIN_CITY", String(255)),
    Column("DEST_CITY", String(255)),
    Column("CRS_DEP_TIME", String(4))
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
                FL_NUMBER=flight[2],
                CRS_DEP_TIME=flight[3],
                ORIGIN_CITY=flight[4],
                DEST_CITY=flight[5]
            )
            connection.execute(query)
            transaction.commit()
    except SQLAlchemyError as e:
        print(f"Database error: {e}")

# Update a flight
def update_flight(flight_number, flight_date, airline, origin_city, dest_city, crs_dep_time):
    try:
        with engine.connect() as connection:
            # Begin a transaction
            transaction = connection.begin()
            query = update(flight_data).where(
                and_(
                    flight_data.c.FL_NUMBER == flight_number,
                    flight_data.c.FL_DATE == flight_date
                )
            ).values(
                AIRLINE=airline,
                ORIGIN_CITY=origin_city,
                DEST_CITY=dest_city,
                CRS_DEP_TIME=crs_dep_time
            )
            result = connection.execute(query)
            transaction.commit()
            if result.rowcount > 0:
                print(f"Updated {result.rowcount} flight(s) successfully.")
                return {"message": "Flight updated successfully"}
            else:
                print("No flight found for the given criteria.")
                return {"message": "No flight found"}
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return {"error": str(e)}

# Delete a flight
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
