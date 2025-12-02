import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from streamlit_elements import elements, mui, html

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Capital Bikeshare brand colors
PRIMARY_RED = "#DA2128"
DARK_RED = "#B71C1C"
LIGHT_RED = "#FFEBEE"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#F5F5F5"
WHITE = "#FFFFFF"

# Page configuration
st.set_page_config(
    page_title="Capital Bikeshare - Demand Prediction",
    page_icon="🚲",
    layout="wide"
)

# Custom CSS
st.markdown(f"""
<style>
    /* Import Material Icons */
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    
    /* FORCE LIGHT MODE - Override all dark mode settings */
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .stApp {{
        color-scheme: light !important;
    }}
    
    /* Force white background everywhere */
    [data-testid="stAppViewContainer"] > div:first-child,
    [data-testid="stApp"] > div:first-child {{
        background-color: white !important;
    }}
    
    /* Material Icons styling */
    .material-icons {{
        font-family: 'Material Icons';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }}


    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
        padding-top: 0.75rem !important;  /* Sesuaikan dengan tinggi button */
    }}
    
    section[data-testid="stSidebar"] .block-container {{
        padding: 0.5rem 1rem 1rem 1rem !important;  /* top right bottom left */
    }}
    
    section[data-testid="stSidebar"] h2 {{
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin: 0 0 1rem 0 !important;
        padding: 0.25rem 0 0.75rem 0 !important;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }}
    
    /* Header bar - MAKE IT RED! */
    .stApp > header {{
        background: linear-gradient(90deg, {PRIMARY_RED} 0%, {DARK_RED} 100%) !important;
    }}
    
    .stApp [data-testid="stHeader"] {{
        background: linear-gradient(90deg, {PRIMARY_RED} 0%, {DARK_RED} 100%) !important;
    }}
    
    .stApp [data-testid="stToolbar"] {{
        color: white !important;
    }}
    
    .stApp [data-testid="stToolbar"] button {{
        color: white !important;
    }}
    
    /* Main background */
    .stApp {{
        background-color: #FAFAFA !important;
    }}
    
    /* Main content area */
    .main .block-container {{
        background-color: #FAFAFA !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 1400px;
    }}
    
    /* Remove default streamlit padding */
    .main {{
        background-color: #FAFAFA !important;
        padding-top: 0 !important;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {PRIMARY_RED} 0%, {DARK_RED} 100%) !important;
        padding-top: 0 !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
        padding-top: 1rem;
        padding-top: 0 !important;
    }}
    
    section[data-testid="stSidebar"] .block-container {{
        padding: 1rem 1rem !important;
    }}
    
    /* Sidebar header */
    section[data-testid="stSidebar"] h2 {{
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-top: 0 !important;  /* Pastikan no margin top */
        padding-top: 0 !important;  /* Pastikan no padding top */
        margin-bottom: 1rem !important;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }}
    
    /* Sidebar text and labels */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: white !important;
    }}
    
    /* Sidebar selectbox */
    section[data-testid="stSidebar"] .stSelectbox {{
        margin-bottom: 1.5rem;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: white !important;
        font-weight: 600;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.5px;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {{
        background-color: white !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        min-height: 48px !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
        background: transparent !important;
        color: {DARK_GRAY} !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        display: flex;
        align-items: center;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox svg {{
        fill: {PRIMARY_RED} !important;
    }}
    
    /* Dropdown menu - FORCE WHITE BACKGROUND & OVERRIDE DARK MODE */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] {{
        background: white !important;
        color-scheme: light !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] > div {{
        background: white !important;
        color-scheme: light !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] ul {{
        background-color: white !important;
        color-scheme: light !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] [role="listbox"] {{
        background-color: white !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
        padding: 4px 0 !important;
        color-scheme: light !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] [role="option"] {{
        background-color: white !important;
        color: {DARK_GRAY} !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
        color-scheme: light !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] [role="option"]:hover {{
        background-color: {LIGHT_RED} !important;
        color: {PRIMARY_RED} !important;
        transform: translateX(4px) !important;
        font-weight: 600 !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] [aria-selected="true"] {{
        background: linear-gradient(90deg, {PRIMARY_RED} 0%, {DARK_RED} 100%) !important;
        color: white !important;
        font-weight: 700 !important;
    }}
    
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="popover"] [aria-selected="true"]:hover {{
        background: linear-gradient(90deg, {PRIMARY_RED} 0%, {DARK_RED} 100%) !important;
        color: white !important;
        transform: translateX(0) !important;
    }}
    
    /* Force light mode for selectbox text in dark mode */
    .stSelectbox [data-baseweb="select"] span {{
        color: {DARK_GRAY} !important;
    }}
    
    /* Override dark mode for dropdown container */
    [data-baseweb="popover"] {{
        color-scheme: light !important;
    }}
    
    /* Sidebar slider */
    section[data-testid="stSidebar"] .stSlider {{
        margin-bottom: 1.5rem;
    }}
    
    section[data-testid="stSidebar"] .stSlider label {{
        color: white !important;
        font-weight: 600;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.5px;
    }}
    
    /* Remove the ugly box around the slider */
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div {{
        background: transparent !important;
    }}
    
    section[data-testid="stSidebar"] .stSlider [role="slider"] {{
        background-color: white !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
        width: 20px !important;
        height: 20px !important;
    }}
    
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] > div {{
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }}
    
    /* Headers */
    .main h1, .main h2, .main h3 {{
        color: {DARK_GRAY} !important;
    }}
    
    /* Hide streamlit branding but keep header visible */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Card styling */
    .card {{
        background: {WHITE};
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: none;
        margin-bottom: 16px;
    }}
    
    /* Force equal height for columns */
    [data-testid="column"] {{
        display: flex !important;
    }}
    
    [data-testid="column"] > div {{
        width: 100% !important;
    }}
    
    [data-testid="column"] .card {{
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    
    /* Prediction box */
    .prediction-box {{
        text-align: center;
        padding: 32px 24px;
        border-radius: 16px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }}
    
    .prediction-number {{
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1;
        letter-spacing: -2px;
    }}
    
    .prediction-label {{
        color: #666;
        font-size: 1.05rem;
        margin-top: 12px;
        font-weight: 500;
    }}
    
    .demand-chip {{
        display: inline-block;
        padding: 10px 28px;
        border-radius: 24px;
        color: white;
        font-weight: 700;
        margin-top: 20px;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        letter-spacing: 0.3px;
    }}
    
    /* Metric card */
    .metric-card {{
        background: {WHITE};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: none;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        transition: transform 0.2s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }}
    
    .metric-icon {{
        font-size: 48px;
        margin-bottom: 12px;
    }}
    
    .metric-icon .material-icons {{
        font-size: 48px;
        color: {PRIMARY_RED};
    }}
    
    .metric-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {DARK_GRAY};
    }}
    
    .metric-label {{
        color: {DARK_GRAY} !important;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 8px;
    }}
    
    /* Info grid */
    .info-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }}
    
    /* Info item */
    .info-item {{
        background: linear-gradient(135deg, {LIGHT_GRAY} 0%, #F8F8F8 100%);
        padding: 14px 18px;
        border-radius: 10px;
        border: 1px solid #ECECEC;
        transition: all 0.2s ease;
    }}
    
    .info-item:hover {{
        background: linear-gradient(135deg, #F0F0F0 0%, #EEEEEE 100%);
        border-color: #E0E0E0;
        transform: translateY(-2px);
    }}
    
    .info-item-label {{
        color: #888;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .info-item-value {{
        color: {DARK_GRAY};
        font-size: 1rem;
        font-weight: 600;
        margin-top: 2px;
    }}
    
    /* Section header */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        margin-top: 8px;
    }}
    
    .section-icon {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, {LIGHT_RED} 0%, #FFE0E0 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: {PRIMARY_RED};
        font-size: 24px;
        box-shadow: 0 2px 8px rgba(218, 33, 40, 0.15);
    }}
    
    .section-icon .material-icons {{
        font-size: 24px;
        color: {PRIMARY_RED};
    }}
    
    .section-title {{
        font-size: 1.35rem;
        font-weight: 700;
        color: {DARK_GRAY} !important;
        margin: 0;
        letter-spacing: -0.3px;
    }}
    
    /* Insight list */
    .insight-list {{
        list-style: none;
        padding: 0;
        margin: 0;
    }}
    
    .insight-item {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid #F0F0F0;
    }}
    
    .insight-item:last-child {{
        border-bottom: none;
    }}
    
    .insight-icon {{
        font-size: 1.5rem;
    }}
    
    .insight-text {{
        flex: 1;
    }}
    
    .insight-primary {{
        font-weight: 600;
        color: {DARK_GRAY};
    }}
    
    .insight-secondary {{
        color: #888;
        font-size: 0.9rem;
    }}
    
    /* Footer */
    .footer {{
        background: linear-gradient(135deg, {DARK_GRAY} 0%, #222222 100%);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin-top: 24px;
        margin-bottom: 0 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }}
    
    .footer-title {{
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 16px;
    }}
    
    .footer-text {{
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    
    .footer-subtext {{
        color: rgba(255,255,255,0.6);
        font-size: 0.85rem;
        margin-top: 8px;
    }}

    
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model_path = os.path.join(SCRIPT_DIR, 'bike_sharing_model.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
    model_loaded = True
except:
    model_loaded = False

# Header Section
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {PRIMARY_RED} 0%, {DARK_RED} 100%);
    border-radius: 15px;
    padding: 40px;
    margin-bottom: 32px;
    box-shadow: 0 12px 40px rgba(218, 33, 40, 0.3);
    text-align: center;
">
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 16px;">
        <div style="
            width: 64px;
            height: 64px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        ">
            <span class="material-icons" style="font-size: 36px; color: {PRIMARY_RED};">pedal_bike</span>
        </div>
        <h1 style="color: white !important; margin: 0; font-weight: 800; font-size: 2.4rem; letter-spacing: -1px;">
            Capital Bikeshare
        </h1>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 12px;">
        <span class="material-icons" style="color: white; font-size: 28px;">insights</span>
        <h2 style="color: white !important; margin: 0; font-weight: 600; font-size: 1.3rem; opacity: 0.95;">
            Demand Prediction System
        </h2>
    </div>
    <p style="color: rgba(255,255,255,0.85); margin-top: 0; font-size: 1rem; line-height: 1.5;">
        Predict bike demand across Metro DC using Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.markdown("## 🚲 Ride Parameters")

# Season with Material Icon-style emoji
season_options = {
    "🌸 Spring": 1,
    "☀️ Summer": 2,
    "🍂 Fall": 3,
    "❄️ Winter": 4
}
season_name = st.sidebar.selectbox("Season", list(season_options.keys()))
season = season_options[season_name]

# Hour
hr = st.sidebar.slider("Hour of Day", 0, 23, 12, format="%d:00")

# Holiday
holiday_options = {"No": 0, "Yes": 1}
holiday_name = st.sidebar.selectbox("Is it a Holiday?", list(holiday_options.keys()))
holiday = holiday_options[holiday_name]

# Weather Situation with Material Icon-style emoji
weather_options = {
    "☀️ Clear / Partly Cloudy": 1,
    "☁️ Mist / Cloudy": 2,
    "🌧️ Light Snow / Light Rain": 3
}
weather_name = st.sidebar.selectbox("Weather Condition", list(weather_options.keys()))
weathersit = weather_options[weather_name]

# Temperature
temp_celsius = st.sidebar.slider("Temperature (°C)", -10, 40, 20)
temp = (temp_celsius + 8) / 47

# Feeling Temperature
atemp_celsius = st.sidebar.slider("Feels Like (°C)", -15, 45, 22)
atemp = (atemp_celsius + 16) / 66

# Humidity
humidity_pct = st.sidebar.slider("Humidity (%)", 0, 100, 50)
hum = humidity_pct / 100

# Main content - Two columns with equal width
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown(f"""
    <div class="card" style="min-height: 510px;">
        <div class="section-header">
            <div class="section-icon"><span class="material-icons">assessment</span></div>
            <h3 class="section-title">Input Summary</h3>
        </div>
        <hr style="margin: 12px 0; background: #E8E8E8;">
        <div class="info-grid">
            <div class="info-item">
                <div class="info-item-label">Season</div>
                <div class="info-item-value">{season_name.split(' ')[-1]}</div>
            </div>
            <div class="info-item">
                <div class="info-item-label">Hour</div>
                <div class="info-item-value">{hr}:00</div>
            </div>
            <div class="info-item">
                <div class="info-item-label">Holiday</div>
                <div class="info-item-value">{holiday_name}</div>
            </div>
            <div class="info-item">
                <div class="info-item-label">Weather</div>
                <div class="info-item-value">{weather_name.split(' ', 1)[-1]}</div>
            </div>
            <div class="info-item">
                <div class="info-item-label">Temperature</div>
                <div class="info-item-value">{temp_celsius}°C</div>
            </div>
            <div class="info-item">
                <div class="info-item-label">Feels Like</div>
                <div class="info-item-value">{atemp_celsius}°C</div>
            </div>
        </div>
        <div class="info-item" style="margin-top: 12px;">
            <div class="info-item-label">Humidity</div>
            <div class="info-item-value">{humidity_pct}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if model_loaded:
        input_data = pd.DataFrame({
            'hum': [hum],
            'weathersit': [weathersit],
            'holiday': [holiday],
            'season': [season],
            'atemp': [atemp],
            'temp': [temp],
            'hr': [hr]
        })
        
        prediction = model.predict(input_data)[0]
        prediction = max(0, round(prediction))
        
        if prediction < 50:
            demand_level = "Low Demand"
            demand_color = "#4CAF50"
            demand_bg = "#E8F5E9"
            recommendation = "Minimal fleet required. Good time for maintenance."
        elif prediction < 150:
            demand_level = "Moderate Demand"
            demand_color = "#FF9800"
            demand_bg = "#FFF3E0"
            recommendation = "Standard fleet deployment recommended."
        elif prediction < 300:
            demand_level = "High Demand"
            demand_color = "#FF5722"
            demand_bg = "#FBE9E7"
            recommendation = "Increase fleet availability. Monitor stock levels."
        else:
            demand_level = "Very High Demand"
            demand_color = PRIMARY_RED
            demand_bg = LIGHT_RED
            recommendation = "Maximum fleet deployment! Prepare for peak traffic."
        
        st.markdown(f"""
        <div class="card" style="min-height: 450px;">
            <div class="section-header">
                <div class="section-icon"><span class="material-icons">trending_up</span></div>
                <h3 class="section-title">Prediction Result</h3>
            </div>
            <hr style="margin: 12px 0; background: #E8E8E8;">
            <div class="prediction-box" style="background: {demand_bg};">
                <div class="prediction-number" style="color: {demand_color};">{prediction}</div>
                <div class="prediction-label">bikes predicted</div>
                <div class="demand-chip" style="background: {demand_color};">{demand_level}</div>
            </div>
            <div style="background: #E3F2FD; border-radius: 8px; padding: 16px; margin-top: 16px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span class="material-icons" style="font-size: 20px; color: #1976D2;">tips_and_updates</span>
                    <strong style="color: {DARK_GRAY};">Recommendation</strong>
                </div>
                <div style="color: #666; font-size: 0.95rem;">{recommendation}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Model not loaded. Please ensure 'bike_sharing_model.pkl' is in the Streamlit folder.")

# Model Performance

st.markdown(f"""
<div class="section-header">
    <div class="section-icon"><span class="material-icons">psychology</span></div>
    <h3 class="section-title">Model Performance</h3>
</div>
""", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><span class="material-icons">smart_toy</span></div>
        <div class="metric-label">Model Type</div>
        <div class="metric-value">XGBoost</div>
        <div style="color: #888; font-size: 0.85rem;">Regressor</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><span class="material-icons">bar_chart</span></div>
        <div class="metric-label">R² Score</div>
        <div class="metric-value" style="color: #4CAF50;">69.76%</div>
        <div style="color: #888; font-size: 0.85rem;">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><span class="material-icons">flash_on</span></div>
        <div class="metric-label">RMSE</div>
        <div class="metric-value" style="color: #FF9800;">97.08</div>
        <div style="color: #888; font-size: 0.85rem;">Error Rate</div>
    </div>
    """, unsafe_allow_html=True)

# Feature Importance
st.markdown(f"""
<div class="section-header">
    <div class="section-icon"><span class="material-icons">bar_chart</span></div>
    <h3 class="section-title">Key Factors Affecting Bike Demand</h3>
</div>
""", unsafe_allow_html=True)

feature_importance_data = pd.DataFrame({
    "Feature": ["Hour of Day", "Temperature", "Season", "Weather", "Feels Like Temp", "Holiday", "Humidity"],
    "Importance": [45, 18, 11, 9, 7, 4, 3]
}).sort_values("Importance", ascending=True)

fig = go.Figure(go.Bar(
    x=feature_importance_data["Importance"],
    y=feature_importance_data["Feature"],
    orientation='h',
    marker_color=PRIMARY_RED,
    text=feature_importance_data["Importance"].astype(str) + '%',
    textposition='outside',
    textfont=dict(size=12, color=DARK_GRAY)
))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=0, r=50, t=10, b=10),
    height=280,
    xaxis=dict(
        showgrid=True,
        gridcolor='#E8E8E8',
        title='',
        range=[0, 55],
        showline=False,
        tickfont=dict(color=DARK_GRAY, size=12)
    ),
    yaxis=dict(
        showgrid=False,
        title='',
        showline=False,
        tickfont=dict(color=DARK_GRAY, size=12)
    ),
    font=dict(family="sans-serif", size=12, color=DARK_GRAY)
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Insights Section
st.markdown(f"""
<div class="section-header">
    <div class="section-icon"><span class="material-icons">lightbulb</span></div>
    <h3 class="section-title">Insights</h3>
</div>
""", unsafe_allow_html=True)

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span class="material-icons" style="font-size: 28px; color: {PRIMARY_RED};">schedule</span>
            <strong style="font-size: 1.1rem; color: {DARK_GRAY};">Peak Demand Hours</strong>
        </div>
        <hr style="margin: 0 0 16px 0; background: #E8E8E8;">
        <ul class="insight-list">
            <li class="insight-item">
                <span class="material-icons" style="font-size: 24px; color: #FF9800;">wb_twilight</span>
                <div class="insight-text">
                    <div class="insight-primary">Morning Rush</div>
                    <div class="insight-secondary">7-9 AM</div>
                </div>
            </li>
            <li class="insight-item">
                <span class="material-icons" style="font-size: 24px; color: {PRIMARY_RED};">nights_stay</span>
                <div class="insight-text">
                    <div class="insight-primary">Evening Rush (Highest)</div>
                    <div class="insight-secondary">5-7 PM</div>
                </div>
            </li>
            <li class="insight-item">
                <span class="material-icons" style="font-size: 24px; color: #4CAF50;">restaurant</span>
                <div class="insight-text">
                    <div class="insight-primary">Lunch Break</div>
                    <div class="insight-secondary">12-1 PM</div>
                </div>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with insights_col2:
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span class="material-icons" style="font-size: 28px; color: {PRIMARY_RED};">wb_sunny</span>
            <strong style="font-size: 1.1rem; color: {DARK_GRAY};">Weather Impact</strong>
        </div>
        <hr style="margin: 0 0 16px 0; background: #E8E8E8;">
        <ul class="insight-list">
            <li class="insight-item">
                <span class="material-icons" style="font-size: 24px; color: #FFC107;">wb_sunny</span>
                <div class="insight-text">
                    <div class="insight-primary">Clear Weather</div>
                    <div class="insight-secondary">Highest demand</div>
                </div>
            </li>
            <li class="insight-item">
                <span class="material-icons" style="font-size: 24px; color: #9E9E9E;">cloud</span>
                <div class="insight-text">
                    <div class="insight-primary">Mist / Cloudy</div>
                    <div class="insight-secondary">~20% decrease</div>
                </div>
            </li>
            <li class="insight-item">
                <span class="material-icons" style="font-size: 24px; color: #2196F3;">grain</span>
                <div class="insight-text">
                    <div class="insight-primary">Rain / Snow</div>
                    <div class="insight-secondary">Significant drop</div>
                </div>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer" style="margin-bottom: 0 !important;">
    <div class="footer-title">Capital Bikeshare Demand Prediction</div>
    <div class="footer-text">Developed by Dede Yudha N (Joey) | Purwadhika Capstone Project 3</div>
    <div class="footer-subtext">XGBoost Regressor | Capital Bikeshare Dataset (2011-2012)</div>
</div>
""", unsafe_allow_html=True)