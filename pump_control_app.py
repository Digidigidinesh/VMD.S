import streamlit as st
import pickle
import pandas as pd
import time

# Load model
@st.cache_resource
def load_model():
    with open('pump_model.pkl', 'rb') as f:
        return pickle.load(f)
    
model = load_model()

# App UI
st.title("🌿 Smart Plant Watering System")
st.subheader("Automated Pump Control Dashboard")

# Input sliders
col1, col2 = st.columns(2)
with col1:
    moisture = st.slider("Soil Moisture Level", 0, 1200, 600, 
                        help="Lower values mean drier soil")
with col2:
    temp = st.slider("Temperature (°C)", 0, 50, 25)

# Prediction
input_data = pd.DataFrame([[moisture, temp]], columns=['moisture', 'temp'])
prediction = model.predict(input_data)[0]
prob = model.predict_proba(input_data)[0]

# Display results
st.subheader("Pump Control Decision")
if prediction == 1:
    st.error("🚨 PUMP ON - Watering Needed")
    # Simulate pump activation
    with st.spinner('Watering in progress...'):
        time.sleep(2)
    st.success("✅ Watering completed!")
else:
    st.success("✅ PUMP OFF - No watering needed")

# Show confidence
st.metric("Confidence Level", 
          f"{max(prob)*100:.1f}%",
          help="Model's confidence in this decision")

# Decision explanation
st.subheader("Decision Factors")
st.write(f"""
- Current Moisture: **{moisture}** (Threshold ~500)
- Current Temperature: **{temp}°C** (Higher temps increase water needs)
- Model Confidence: **{max(prob)*100:.1f}%**
""")

# Historical data simulation
if st.checkbox("Show simulated sensor data"):
    chart_data = pd.DataFrame({
        'Moisture': [moisture] * 5 + [400, 800],
        'Temperature': [temp] * 5 + [20, 35]
    })
    st.line_chart(chart_data)

# Footer
st.markdown("---")
st.caption("Automated Plant Watering System v1.0 | Pump control simulated for demonstration")
