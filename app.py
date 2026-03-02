import streamlit as st
import pandas as pd
import joblib

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Solar Energy Forecasting",
    page_icon="☀️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- global ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* dark background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e);
    color: #e2e8f0;
}

/* ---------- hero banner ---------- */
.hero {
    background: linear-gradient(135deg, #f7971e, #ffd200, #f7971e);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(247,151,30,0.35);
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    color: #1a1a2e;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1rem;
    color: #2d2d2d;
    margin-top: 0.5rem;
    margin-bottom: 0;
}

/* ---------- section cards ---------- */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.4rem;
    backdrop-filter: blur(12px);
}
.card-title {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #ffd200;
    margin-bottom: 1rem;
}

/* ---------- metric chips ---------- */
.chip-row {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 0.5rem;
}
.chip {
    background: rgba(247,151,30,0.15);
    border: 1px solid rgba(247,151,30,0.3);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    color: #ffd200;
    font-weight: 600;
}

/* ---------- predict button ---------- */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #f7971e, #ffd200) !important;
    color: #1a1a2e !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 20px rgba(247,151,30,0.4) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(247,151,30,0.55) !important;
}

/* ---------- result banner ---------- */
.result-box {
    background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(16,185,129,0.15));
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    animation: fadeSlideUp 0.5s ease forwards;
    margin-top: 1.2rem;
}
.result-value {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #22c55e, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.result-label {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 0.4rem;
    letter-spacing: 0.5px;
}

@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---------- sliders & inputs ---------- */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, #f7971e, #ffd200) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #cbd5e1 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ---------- selectbox ---------- */
div[data-testid="stSelectbox"] > div {
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.06) !important;
}

/* hide default streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>☀️ Solar Energy Forecasting</h1>
    <p>AI-powered AC power prediction for solar plants</p>
</div>
""", unsafe_allow_html=True)

# ── Plant selection ────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">⚡ Plant Selection</div>', unsafe_allow_html=True)
plant_choice = st.selectbox("Select Plant", ["Plant 1", "Plant 2"], label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# Load correct model
if plant_choice == "Plant 1":
    model = joblib.load("model_plant1.pkl")
else:
    model = joblib.load("model_plant2.pkl")

# ── Layout columns ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card"><div class="card-title">🕐 Time Features</div>', unsafe_allow_html=True)
    hour  = st.slider("Hour of Day",   0, 23,  12)
    day   = st.slider("Day of Month",  1, 31,  15)
    month = st.slider("Month",         1, 12,   6)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="card-title">🌡️ Weather Conditions</div>', unsafe_allow_html=True)
    irradiation  = st.number_input("Irradiation (W/m²)",        value=0.5,  format="%.3f")
    ambient_temp = st.number_input("Ambient Temperature (°C)",  value=25.0, format="%.1f")
    module_temp  = st.number_input("Module Temperature (°C)",   value=30.0, format="%.1f")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Historical AC power ────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📊 Historical AC Power (kW)</div>', unsafe_allow_html=True)
hcol1, hcol2, hcol3 = st.columns(3)
with hcol1:
    prev_1  = st.number_input("1 Hour Ago",   value=100.0, format="%.1f")
with hcol2:
    prev_2  = st.number_input("2 Hours Ago",  value=100.0, format="%.1f")
with hcol3:
    prev_24 = st.number_input("24 Hours Ago", value=100.0, format="%.1f")
st.markdown("</div>", unsafe_allow_html=True)

roll_3 = (prev_1 + prev_2 + prev_24) / 3

# ── Input summary chips ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="chip-row">
    <span class="chip">🕐 {hour:02d}:00</span>
    <span class="chip">📅 {day:02d}/{month:02d}</span>
    <span class="chip">☀️ Irr: {irradiation:.3f}</span>
    <span class="chip">🌡️ Amb: {ambient_temp:.1f}°C</span>
    <span class="chip">🔆 Mod: {module_temp:.1f}°C</span>
    <span class="chip">📈 Roll Avg: {roll_3:.1f} kW</span>
</div>
""", unsafe_allow_html=True)

# ── Predict ────────────────────────────────────────────────────────────────────
if st.button("⚡ Predict AC Power"):
    input_dict = {
        'AMBIENT_TEMPERATURE': ambient_temp,
        'MODULE_TEMPERATURE':  module_temp,
        'IRRADIATION':         irradiation,
        'hour':                hour,
        'day':                 day,
        'month':               month,
        'ac_power_prev_1':     prev_1,
        'ac_power_prev_24':    prev_24,
        'ac_power_prev_2':     prev_2,
        'ac_power_roll_3':     roll_3,
    }

    input_data = pd.DataFrame([input_dict])[model.feature_names_in_]
    prediction = model.predict(input_data)[0]

    st.markdown(f"""
    <div class="result-box">
        <div class="result-value">{prediction:,.2f} <span style="font-size:1.2rem;-webkit-text-fill-color:#10b981;">kW</span></div>
        <div class="result-label">Predicted AC Power Output · {plant_choice}</div>
    </div>
    """, unsafe_allow_html=True)