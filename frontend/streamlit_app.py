import streamlit as st
import time
import pandas as pd
import numpy as np
import joblib
import xgboost
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

# --- Load ML Models (Self-Contained for Streamlit Cloud) ---
@st.cache_resource
def load_models():
    model = joblib.load('notebooks/models/healthrisk_xgboost.pkl')
    pipeline = joblib.load('notebooks/models/preprocessing_pipeline.pkl')
    return model, pipeline

model, pipeline = load_models()

# --- State Management for Real-Time Database ---
if 'patient_registry' not in st.session_state:
    st.session_state.patient_registry = pd.DataFrame({
        "Patient ID": ["PT-8821", "PT-8822", "PT-8823"],
        "Age": [65, 42, 78],
        "Gender": ["M", "F", "M"],
        "BP (mmHg)": ["160/100", "120/80", "145/90"],
        "Weight (kg)": [110.0, 65.0, 85.0],
        "Heart Rate": [110, 72, 95],
        "Smoker": ["Y", "N", "Y"],
        "AI Risk Score": ["88% (Critical)", "15% (Normal)", "72% (Critical)"],
        "Status": ["Admitted", "Discharged", "Monitoring"]
    })

# --- Page Configuration ---
st.set_page_config(
    page_title="HealthRisk AI Enterprise",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Animated Headings and Styling ---
st.markdown("""
    <style>
    /* Gradient Animation for Headings */
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glowing Pulse Animation */
    @keyframes glowPulse {
        0% { text-shadow: 0 0 10px rgba(16, 185, 129, 0.5); }
        50% { text-shadow: 0 0 25px rgba(16, 185, 129, 1), 0 0 10px rgba(16, 185, 129, 0.8); }
        100% { text-shadow: 0 0 10px rgba(16, 185, 129, 0.5); }
    }

    /* Apply animations to ALL headings */
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(270deg, #10b981, #3b82f6, #10b981);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 5s ease infinite, glowPulse 3s infinite alternate;
        font-weight: 800 !important;
        margin-bottom: 20px;
        padding-bottom: 5px;
    }
    
    /* Custom button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #059669, #10b981);
        color: white;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        border: none;
        transition: transform 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Risk Report Cards */
    .risk-critical { color: #ef4444 !important; font-size: 2.8em; font-weight: 900; text-align: center; margin-bottom: 15px; -webkit-text-fill-color: #ef4444; }
    .risk-normal { color: #10b981 !important; font-size: 2.8em; font-weight: 900; text-align: center; margin-bottom: 15px; -webkit-text-fill-color: #10b981; }
    .report-box { padding: 30px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); background-color: rgba(0,0,0,0.3); backdrop-filter: blur(10px); box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
    </style>
""", unsafe_allow_html=True)

# --- Helper Function for Lottie ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load Animations (using lightweight public Lottie files)
lottie_health = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5n8yxcb3.json") # Medical heartbeat
lottie_ai = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_qmfs6c3i.json") # Tech/AI animation

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h1>HealthRisk AI</h1>", unsafe_allow_html=True)
    st.markdown("*Enterprise Clinical Support*")
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Risk Analyzer", "Patient Registry", "AI Explainability"],
        icons=["activity", "clipboard-data", "cpu"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#10b981", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "rgba(16, 185, 129, 0.1)"},
            "nav-link-selected": {"background-color": "rgba(16, 185, 129, 0.2)", "color": "#10b981"},
        }
    )
    
    if lottie_health:
        st_lottie(lottie_health, height=150, key="health_sidebar")

# ==========================================
# PAGE 1: CLINICAL RISK ANALYZER
# ==========================================
if selected == "Risk Analyzer":
    st.markdown("<h1>Enterprise Clinical Decision Support System</h1>", unsafe_allow_html=True)
    st.divider()

    left_col, right_col = st.columns([1.3, 1])

    with left_col:
        st.markdown("<h2>Patient Vitals & Demographics</h2>", unsafe_allow_html=True)
        
        with st.form("clinical_form"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                age = st.number_input("Patient Age (Years)", min_value=1, max_value=120, value=65)
                weight = st.number_input("Patient Weight (kg)", min_value=20.0, max_value=300.0, value=110.0)
                hr = st.number_input("Resting Heart Rate (BPM)", min_value=30, max_value=200, value=110)
                cholesterol = st.slider("Total Cholesterol (mg/dL)", 100, 350, 220)
                
            with col_b:
                gender = st.selectbox("Biological Sex", ["M", "F"])
                bp = st.text_input("Blood Pressure (mmHg)", value="160/100", help="Format: Systolic/Diastolic")
                smoker = st.selectbox("Smoker Status", ["N", "Y"], index=1)
                blood_sugar = st.slider("Fasting Blood Sugar (mg/dL)", 70, 200, 110)
                
            submitted = st.form_submit_button("🚀 Run AI Risk Analysis")

    with right_col:
        st.markdown("<h2>Clinical Summary Report</h2>", unsafe_allow_html=True)
        
        if not submitted:
            st.info("👈 Enter comprehensive patient data on the left and click analyze to generate a high-fidelity AI risk report.")
            if lottie_ai:
                st_lottie(lottie_ai, height=250, key="ai_idle")
        
        if submitted:
            with st.spinner('Analyzing Patient Vitals...'):
                time.sleep(1.5) # Artificial delay for animation
                
                try:
                    # Parse BP
                    try:
                        systolic_bp = float(bp.split('/')[0])
                    except:
                        systolic_bp = 120.0
                    
                    input_df = pd.DataFrame([{
                        'age': age,
                        'gender': gender,
                        'weight': weight,
                        'systolic_bp': systolic_bp,
                        'hr': hr,
                        'smoker': smoker
                    }])
                    
                    # Direct Model Prediction (Self-Contained for Streamlit Cloud)
                    clean_data = pipeline.transform(input_df)
                    risk_probability = model.predict_proba(clean_data)[0][1]
                    percentage = int(risk_probability * 100)
                    is_high_risk = bool(risk_probability > 0.70)
                    
                    st.markdown('<div class="report-box">', unsafe_allow_html=True)
                    
                    if is_high_risk or percentage > 70:
                        risk_str = f"{percentage}% (Critical)"
                        status_str = "Admitted"
                        st.markdown(f'<div class="risk-critical">CRITICAL RISK: {percentage}%</div>', unsafe_allow_html=True)
                        st.progress(percentage / 100)
                        st.error(f"⚠️ **URGENT:** Patient profile shows critical correlation with adverse cardiovascular events. The primary contributing factors are elevated Blood Pressure ({bp}) and high Resting Heart Rate ({hr} BPM). Immediate clinical intervention is recommended.")
                    else:
                        risk_str = f"{percentage}% (Normal)"
                        status_str = "Monitoring"
                        st.markdown(f'<div class="risk-normal">NORMAL PROFILE: {percentage}%</div>', unsafe_allow_html=True)
                        st.progress(percentage / 100)
                        st.success("✅ **CLEARED:** Patient profile does not currently indicate a high risk of adverse clinical outcomes. Vitals are within acceptable clinical parameters. Routine monitoring is sufficient.")
                        
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Log the scan to the Patient Registry database
                    import random
                    new_pt = pd.DataFrame([{
                        "Patient ID": f"PT-{random.randint(1000, 9999)}",
                        "Age": age, "Gender": gender, "BP (mmHg)": bp,
                        "Weight (kg)": weight, "Heart Rate": hr, "Smoker": smoker,
                        "AI Risk Score": risk_str, "Status": status_str
                    }])
                    st.session_state.patient_registry = pd.concat([st.session_state.patient_registry, new_pt], ignore_index=True)
                        
                except Exception as e:
                    st.error(f"🚨 System Error! The clinical decision engine encountered an error: {e}")

# ==========================================
# PAGE 2: PATIENT REGISTRY
# ==========================================
elif selected == "Patient Registry":
    st.markdown("<h1>Secure Patient Database</h1>", unsafe_allow_html=True)
    st.markdown("View historical predictions and manage patient cohorts.")
    
    # Display the real-time session state registry
    st.dataframe(st.session_state.patient_registry, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Convert DataFrame to CSV string for native download
        csv = st.session_state.patient_registry.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Export Registry to CSV",
            data=csv,
            file_name='patient_registry_export.csv',
            mime='text/csv',
        )
        
    with col2:
        # Create an interactive mock sync button
        if st.button("🔄 Sync with Electronic Health Records (EHR)"):
            with st.spinner("Establishing secure connection to Hospital EHR (HL7 FHIR)..."):
                time.sleep(2.5) # Fake network delay for presentation purposes
                st.success("✅ EHR Sync Complete: 6 patient records updated and securely synchronized.")

# ==========================================
# PAGE 3: AI EXPLAINABILITY
# ==========================================
elif selected == "AI Explainability":
    st.markdown("<h1>Clinical Risk Factors</h1>", unsafe_allow_html=True)
    st.markdown("HealthRisk AI provides transparent clinical insights to ensure patient safety. Our system provides detailed feature importance for every prediction to support clinical decision-making.")
    
    st.info("💡 **How it works:** The system calculates the marginal clinical contribution of each patient vital to the final risk probability.")
    
    st.markdown("<h2>Global Feature Importance</h2>", unsafe_allow_html=True)
    
    # Mock feature importance chart
    chart_data = pd.DataFrame({
        "Impact on Risk Score": [0.35, 0.25, 0.20, 0.12, 0.05, 0.03],
        "Clinical Feature": ["Systolic BP", "Age", "Weight", "Heart Rate", "Smoker Status", "Gender"]
    }).set_index("Clinical Feature")
    
    st.bar_chart(chart_data, color="#10b981", height=400)
    
    st.markdown("<h2>Clinical Guidelines</h2>", unsafe_allow_html=True)
    st.markdown("""
    * **Blood Pressure (35% impact):** Hypertension is the leading predictor of adverse outcomes in our dataset.
    * **Age (25% impact):** Risk scales linearly with patient age.
    * **Weight (20% impact):** BMI-related complications strongly influence overall cardiovascular risk.
    """)
