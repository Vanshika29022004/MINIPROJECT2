import streamlit as st
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="Cardiac Arrest Monitoring System",
    page_icon="🫀",
    layout="centered"
)

# Title
st.title("🫀 Real-Time Cardiac Arrest Documentation & Clinical Guidance")
st.markdown("### Frontend Interface (Tanya )")

st.divider()

# Patient details
st.subheader("👤 Patient Details")
patient_name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

st.divider()

# Simulated vitals
st.subheader("📊 Real-Time Vital Signs")

if st.button("Generate Vitals"):
    heart_rate = random.randint(0, 120)
    spo2 = random.randint(60, 100)
else:
    heart_rate = 72
    spo2 = 98

st.metric("Heart Rate (bpm)", heart_rate)
st.metric("SpO₂ (%)", spo2)

st.divider()

# Analyze button
if st.button("Analyze Patient Condition"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.subheader("🕒 Analysis Time")
    st.write(current_time)

    if heart_rate <= 0 or spo2 < 70:
        st.error("🚨 CARDIAC ARREST DETECTED!")

        st.subheader("🚑 Clinical Guidance")
        st.write("1️⃣ Call emergency services immediately")
        st.write("2️⃣ Start CPR (30 chest compressions)")
        st.write("3️⃣ Give 2 rescue breaths")
        st.write("4️⃣ Use AED if available")
        st.write("5️⃣ Continue until help arrives")

    else:
        st.success("✅ Patient is Stable")
        st.write("✔ Continue monitoring vital signs")
        st.write("✔ Maintain oxygen supply if required")

st.divider()

# Footer
st.caption("Frontend Prototype | Academic Project | Tanya (Team Leader)")