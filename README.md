# Flight Delay Prediction

Check out the app here! https://flighdelayprediction.streamlit.app/

## Steps for Local Setup

1. Clone the repo
2. Navigate to `phase-3` folder
3. Run `pip install -r requirements.txt`
4. Install SQLite
5. Run `sqlite3 flight_data.db` - This creates the table named `flight_data` and also loads the `flight_data.csv` data into the table
6. To start the app, run `streamlit run flight_delay_app.py`

## 🚀 Tech Stack

### **Frontend**
- **Streamlit**: Simple and interactive UI for the web app, handling user inputs and displaying predictions.

### **Backend**
- **Python**: Core language for application logic, model loading, and data processing.

### **Machine Learning**
- **CatBoost**: Gradient boosting library for predicting flight delays.
- **Joblib**: For saving and loading the trained CatBoost model.
- **SMOTE**: To handle class imbalance in the training dataset.
- **Scikit-Learn**: For preprocessing, splitting data, and evaluation metrics.

### **Database**
- **SQLite**: Lightweight local database for storing flight data when running the app locally.
- **SQLAlchemy**: ORM for interacting with the database using Python.
- **AWS RDS (MySQL)**: Cloud-based database solution for deployed applications.

### **Data Processing**
- **Pandas**: For handling and manipulating datasets.
- **NumPy**: For numerical operations and computations.

### **Deployment**
- **Streamlit Cloud**: Hosting the web app for public access.
- **Google Drive**: Storing large model files (`.pkl.gz`) to overcome Git LFS bandwidth limits.
