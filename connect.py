import pyodbc
import pandas as pd
import streamlit as st

# Replace these values with your SQL Server details
server = 'DESKTOP-MBAD9GI'  # Update with your server name
database = 'Patient'        # Update with your database name

# Database connection function
def connect_to_database():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None

# Save Patient Data to Database
def save_patient_data(conn, data):
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO Patient_info (first_name, last_name, age, gender, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, data)
        conn.commit()
        st.success("Patient data saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {str(e)}")

# Streamlit UI
st.title('Diabetes Prediction Web App')

# Collect Patient Details
with st.container():
    st.header('Enter Your Details')
    col1, col2 = st.columns(2)

    with col1:
        f_name = st.text_input("First Name")
        Gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        SmokingHistory = st.selectbox("Smoking History", ["never", "current", "former", "not known"])
        Hypertension = st.selectbox("Hypertension", ["Yes", "No"])
        HeartDisease = st.selectbox("Heart Disease", ["Yes", "No"])

    with col2:
        l_name = st.text_input("Last Name")
        Age = st.slider("Age", 0, 120, 25)
        BMI = st.slider("BMI", 10.0, 50.0, 22.0)
        HbA1cLevel = st.slider("HbA1c Level", 3.0, 15.0, 5.5)
        BloodGlucoseLevel = st.slider("Blood Glucose Level", 50.0, 300.0, 100.0)

# Encode Inputs
gender_encoding = {'Male': 0, 'Female': 1, 'Other': 2}
smoking_history_encoding = {'never': 0, 'current': 1, 'former': 2, 'not known': 3}
hypertension_encoding = {'Yes': 1, 'No': 0}
heart_disease_encoding = {'Yes': 1, 'No': 0}

gender_encoded = gender_encoding[Gender]
smoking_history_encoded = smoking_history_encoding[SmokingHistory]
hypertension_encoded = hypertension_encoding[Hypertension]
heart_disease_encoded = heart_disease_encoding[HeartDisease]

input_data = pd.DataFrame({
    'first_name': [f_name],
    'last_name': [l_name],
    'age': [Age],
    'gender': [gender_encoded],
    'hypertension': [hypertension_encoded],
    'heart_disease': [heart_disease_encoded],
    'smoking_history': [smoking_history_encoded],
    'bmi': [BMI],
    'HbA1c_level': [HbA1cLevel],
    'blood_glucose_level': [BloodGlucoseLevel]
})

# Automatically Save Data
conn = connect_to_database()
if conn:
    save_patient_data(conn, (
        f_name, l_name, Age, gender_encoded, hypertension_encoded, heart_disease_encoded, smoking_history_encoded, BMI, HbA1cLevel, BloodGlucoseLevel
    ))
    conn.close()

    st.experimental_rerun()  # Refresh the page to clear form inputs

# Display the submitted data
st.write("Patient Information Preview:")
st.dataframe(input_data)