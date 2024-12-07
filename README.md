# Flight Delay Prediction

This application has been developed and deployed using `streamlit`. The database has been hosted on AWS RDS.
Check out the app here! https://flighdelayprediction.streamlit.app/

## Steps for Local Setup

1. Ensure to have Python 3.x setup in local
2. Clone the repo
3. Navigate to `phase-3` folder
4. Run `pip install -r requirements.txt`
5. Install SQLite **if not present** in your system. MacOS has SQLite by default, and Windows systems having python 3.x will already have sqlite.
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
