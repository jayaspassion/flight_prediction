# Flight Delay Prediction

Steps for Local Setup

1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Create a folder called `.streamlit` and within it, create a file named `secrets.toml` with the DATABASE_URL content
    a. For local sqlite database, copy the below content:
        DATABASE_URL = "sqlite:///flight_data.db"
4. To start the app, run `streamlit run flight_delay_app.py`
