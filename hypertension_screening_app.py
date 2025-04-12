# -*- coding: utf-8 -*-
"""Hypertension Screening App.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yUvy9iqLQXnyK9jos2Onupo9gF7QBLGm
"""

import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('hypertension_model.pkl')

# App title and description
st.title("Hypertension Risk Prediction")
st.markdown("Predict hypertension risk based on health and demographic factors")

def user_input_features():
    st.sidebar.header("Patient Input Features")

    # ====== Collect Inputs ======
    # Demographic Info
    age = st.sidebar.selectbox("Age", ["18-24", "25-29", "30-34", "35-39", "40-44",
                                  "45-49", "50-54", "55-59", "60-64", "65-69",
                                  "70-74", "75-79", "80+"])
    sex = st.sidebar.radio("Sex", ["Male", "Female"])
    tribe = st.sidebar.selectbox("Tribe", ["Ibibio", "Igbo", "Yoruba", "Tiv", "Hausa Fulani", "Other"])

    # Health Behaviors
    PhysicalActivity = st.sidebar.radio("Physical Activity", ["Yes", "No"])
    bmi_category = st.sidebar.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])
    gen_health = st.sidebar.selectbox("General Health", ["Poor", "Fair", "Good", "Very good", "Excellent"])

    # Health Metrics
    PhysicalHealth = st.sidebar.number_input("Physical Health (Last 30 Days)", 0, 30, 5)
    MentalHealth = st.sidebar.number_input("Mental Health (Last 30 Days)", 0, 30, 5)
    sleep_time = st.sidebar.number_input("Sleep Time (hours)", 2, 16, 7)

    # Medical History
    alcohol = st.sidebar.radio("Alcohol Drinking", ["No", "Yes"])
    smoking = st.sidebar.radio("Smoking Status", ["No", "Yes"])
    skin_cancer = st.sidebar.radio("Skin Cancer", ["No", "Yes"])
    diabetics = st.sidebar.radio("Diabetic", ["No", "Yes"])
    diff_walking = st.sidebar.radio("Difficulty Walking", ["No", "Yes"])
    asthma = st.sidebar.radio("Asthma", ["No", "Yes"])
    kidney_disease = st.sidebar.radio("Kidney Disease", ["No", "Yes"])
    stroke = st.sidebar.radio("History of Stroke", ["No", "Yes"])

    # ====== Encode Inputs ======
    # Age Category Encoding (example mapping - verify with your training data)
    age_mapping = {
        "18-24": 0, "25-29": 1, "30-34": 2, "35-39": 3,
        "40-44": 4, "45-49": 5, "50-54": 6, "55-59": 7,
        "60-64": 8, "65-69": 9, "70-74": 10, "75-79": 11, "80+": 12
    }

    # General Health Encoding
    gen_health_mapping = {
        "Poor": 0, "Fair": 1, "Good": 2, "Very good": 3, "Excellent": 4
    }

    # Physical/Mental Health Category Encoding
    def health_category_encoder(value):
        if value < 5: return 0      # None
        elif 5 <= value < 10: return 1  # Mild
        elif 10 <= value < 20: return 2 # Moderate
        else: return 3               # Severe

    input_data = {
        # Binary Features
        "Smoking": 1 if smoking == "Yes" else 0,
        "AlcoholDrinking": 1 if alcohol == "Yes" else 0,
        "Stroke": 1 if stroke == "Yes" else 0,
        "DiffWalking": 1 if diff_walking == "Yes" else 0,
        "Sex": 1 if sex == "Male" else 0,
        "Diabetic": 1 if diabetics == "Yes" else 0,
        "PhysicalActivity": 1 if PhysicalActivity == "Yes" else 0,
        "SleepTime": sleep_time,
        "Asthma": 1 if asthma == "Yes" else 0,
        "KidneyDisease": 1 if kidney_disease == "Yes" else 0,
        "SkinCancer": 1 if skin_cancer == "Yes" else 0,

        # BMI Categories (one-hot encoded)
        "BMI_category_Normal": 1 if bmi_category == "Normal" else 0,
        "BMI_category_Overweight": 1 if bmi_category == "Overweight" else 0,
        "BMI_category_Obese": 1 if bmi_category == "Obese" else 0,

        # Tribe (one-hot encoded)
        "Tribe_Ibibio": 1 if tribe == "Ibibio" else 0,
        "Tribe_Igbo": 1 if tribe == "Igbo" else 0,
        "Tribe_Other": 1 if tribe in ["Hausa Fulani", "Other"] else 0,
        "Tribe_Tiv": 1 if tribe == "Tiv" else 0,
        "Tribe_Yoruba": 1 if tribe == "Yoruba" else 0,

        # Encoded Numerical Features
        "AgeCategory_encoded": age_mapping[age],
        "GenHealth_encoded": gen_health_mapping[gen_health],
        "PhysicalHealth_Category_encoded": health_category_encoder(PhysicalHealth),
        "MentalHealth_Category_encoded": health_category_encoder(MentalHealth)
    }

    return pd.DataFrame(input_data, index=[0])

# Get user input
input_df = user_input_features()

# Display input data
st.subheader("Patient Input Data")
st.write(input_df)

# Predict
prediction = model.predict(input_df)
pred_prob = model.predict_proba(input_df)[:, 1][0]

# Display results
st.subheader("Prediction")
st.write(f"**Probability of Hypertension:** {pred_prob:.2%}")
st.write(f"**Predicted Class:** {'High Risk' if prediction[0] == 1 else 'Low Risk'}")

# Color-coded message + recommendation
if predicted_class == "High Risk":
    st.markdown(
        "<div style='color:red; font-size:20px; font-weight:bold;'>⚠️ High Risk of Hypertension</div>", 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        **Recommendations:**
        - Please consult a healthcare provider for a proper check-up.  
        - Maintain a healthy diet, reduce salt intake, and exercise regularly.  
        - Monitor your blood pressure frequently.
        """
    )
else:
    st.markdown(
        "<div style='color:green; font-size:20px; font-weight:bold;'>✅ Low Risk of Hypertension</div>", 
        unsafe_allow_html=True
    )
    st.markdown(
        """
        **Recommendations:**
        - Keep up with your healthy lifestyle habits!  
        - Get regular health check-ups.  
        - Stay active and eat balanced meals.
        """
    ))
