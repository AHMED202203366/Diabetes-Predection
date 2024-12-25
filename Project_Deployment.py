import pickle
import streamlit as st
import pandas as pd

# Clear the cache
st.cache_data.clear()

# Load the pre-trained model
data = pickle.load(open("D:\\VS Code\\Project Software\\Diabetes_Pred.sav", 'rb'))

# Title and Info
st.title('Diabetes Prediction Web App')
st.markdown("""
<style>
    body {
        background-color: #f4f4f4;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
        color: white;
    }
</style>
""", unsafe_allow_html=True)
st.info('An Easy Application for Predicting Diabetes Disease')

# Layout Structure
with st.container():
    st.header('Enter Patient Details')
    
    # Divide inputs into two columns
    col1, col2 = st.columns(2)

    # Inputs in Column 1
    with col1:
        f_name = st.text_input("Enter Your First Name")
        Gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        SmokingHistory = st.selectbox("Smoking History", ["never", "current", "former", "not known"])
        Hypertension = st.selectbox("Hypertension (Yes or No)", ["Yes", "No"])
        HeartDisease = st.selectbox("Heart Disease (Yes or No)", ["Yes", "No"])

    # Inputs in Column 2
    with col2:
        l_name = st.text_input("Enter Your Last Name")
        Age = st.slider("Age", 0, 120, 25)  # Slider with range 0 to 120
        BMI = st.slider("BMI", 10.0, 50.0, 22.0)  # Slider with range 10.0 to 50.0
        HbA1cLevel = st.slider("HbA1c Level", 3.0, 15.0, 5.5)  # Slider with range 3.0 to 15.0
        BloodGlucoseLevel = st.slider("Blood Glucose Level", 50.0, 300.0, 100.0)  # Slider with range 50.0 to 300.0

# Encode categorical features
gender_encoding = {'Male': 0, 'Female': 1, 'Other': 2}
smoking_history_encoding = {
    'never': 0, 
    'current': 1, 
    'former': 2, 
    'not known': 3
}
hypertension_encoding = {'Yes': 1, 'No': 0}
heart_disease_encoding = {'Yes': 1, 'No': 0}

# Encode user inputs
try:
    gender_encoded = gender_encoding[Gender]
    smoking_history_encoded = smoking_history_encoding[SmokingHistory]
    hypertension_encoded = hypertension_encoding[Hypertension]
    heart_disease_encoded = heart_disease_encoding[HeartDisease]

    # Create input data for the model
    input_data = pd.DataFrame({
        'gender': [gender_encoded],
        'age': [Age],
        'hypertension': [hypertension_encoded],
        'heart_disease': [heart_disease_encoded],
        'smoking_history': [smoking_history_encoded],
        'bmi': [BMI],
        'HbA1c_level': [HbA1cLevel],
        'blood_glucose_level': [BloodGlucoseLevel]
    })
except ValueError:
    st.error("Please ensure all numerical fields are correctly filled!")

# Prediction Button
with st.container():
    predict_button = st.button("Predict Diabetes")
    if predict_button:
        try:
            result = data.predict(input_data)
            st.markdown("---")
            with st.sidebar:
                if result[0] == 0:
                    st.success('The Patient Is Clear')
                    st.image("D:\VS Code\Project Software\Screenshot 2024-10-24 130623.png", width=300)
                else:
                    st.error('The Patient Has Diabetes')
                    st.image("D:\VS Code\Project Software\Screenshot 2024-10-22 231216.png", width=300)
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
