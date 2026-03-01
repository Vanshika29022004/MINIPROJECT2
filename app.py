import streamlit as st
from datetime import datetime
import random


st.set_page_config(
    page_title="Cardiac Arrest Monitoring System",
    page_icon="🫀",
    layout="centered"
)

# Ttitle
st.title(" Real-Time Cardiac Arrest Documentation & Clinical Guidance")
st.markdown("### Frontend Interface (Tanya)")

st.divider()

#patient details
st.subheader(" Patient Details")
patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

st.divider()

# real time virtual signs
st.subheader(" Real-Time Vital Signs")

# Default values
heart_rate = 72
spo2 = 98

# Normal vitals simulation
if st.button("Generate Normal Vitals"):
    heart_rate = random.randint(60, 100)
    spo2 = random.randint(95, 100)

# Emergency test cases
st.subheader(" Emergency Test Cases")

col1, col2 = st.columns(2)

with col1:
    if st.button("Simulate Cardiac Arrest"):
        heart_rate = 0
        spo2 = 65

with col2:
    if st.button("Simulate Severe Hypoxia"):
        heart_rate = 80
        spo2 = 60

# Display vitals
st.metric("Heart Rate (bpm)", heart_rate)
st.metric("SpO₂ (%)", spo2)

st.divider()

# Analyse patient condition
if st.button("Analyze Patient Condition"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.subheader(" Analysis Time")
    st.write(current_time)

    # Cardiac arrest logic
    if heart_rate <= 0 or spo2 < 70:
        st.error(" CARDIAC ARREST DETECTED!")

        st.subheader(" Clinical Guidance")
        st.write("1️ Call emergency services immediately")
        st.write("2️ Start CPR (30 chest compressions)")
        st.write("3️ Give 2 rescue breaths")
        st.write("4️ Use AED if available")
        st.write("5️ Continue until medical help arrives")

    else:
        st.success(" Patient is Stable")
        st.write(" Continue monitoring vital signs")
        st.write(" Maintain oxygen supply if required")

st.divider()


st.info(" This is an academic prototype. Emergency values are simulated.")
st.caption("Frontend Prototype | Academic Project | Tanya (Team Leader)")




