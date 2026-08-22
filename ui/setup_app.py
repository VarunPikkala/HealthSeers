import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

requirements = """streamlit==1.32.0
pandas==2.2.1
numpy==1.26.4
plotly==5.19.0
pydeck==0.8.1b0
scikit-learn==1.4.1.post1
tensorflow==2.15.0
"""

style_css = """
/* Base styles */
body {
    background-color: #f8f9fa;
    color: #1e293b;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit default UI elements */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}

/* General Container Padding */
.block-container {
    padding-top: 1rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1400px;
}

/* Header Container */
.header-container {
    background-color: #ffffff;
    padding: 15px 30px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.header-logo {
    display: flex;
    align-items: center;
    gap: 15px;
}

.header-title {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
}

.header-subtitle {
    font-size: 14px;
    color: #0ea5e9;
    font-weight: 600;
    margin: 0;
}

.header-desc {
    font-size: 13px;
    color: #64748b;
    max-width: 300px;
    line-height: 1.4;
    margin-left: 20px;
    padding-left: 20px;
    border-left: 1px solid #e2e8f0;
}

.header-stages {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    font-weight: 600;
    color: #475569;
}

.stage-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #0f172a !important;
}
[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
}

/* KPI Cards */
.kpi-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    text-align: center;
}
.kpi-title {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 5px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 0;
}
.kpi-subtitle {
    font-size: 12px;
    color: #94a3b8;
}

.risk-high { color: #ef4444; }
.risk-medium { color: #f59e0b; }
.risk-low { color: #10b981; }

.badge-high { background-color: #fecaca; color: #991b1b; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight:bold;}
.badge-medium { background-color: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight:bold;}
.badge-low { background-color: #d1fae5; color: #065f46; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight:bold;}

/* Generic Card */
.generic-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.card-title {
    font-size: 14px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 15px;
    text-transform: uppercase;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 8px;
}

.alert-summary-card {
    background-color: #fef2f2;
    border: 1px solid #fecaca;
}

.architecture-strip {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 20px;
    border-radius: 8px;
    margin-top: 30px;
}
.arch-stage {
    text-align: center;
    font-size: 12px;
}
"""

data_loader_py = """import pandas as pd
import numpy as np
import streamlit as st
import datetime

@st.cache_data
def load_demo_data():
    np.random.seed(42)
    
    # Generate mock districts (India bounding box roughly)
    states = ["Assam", "Meghalaya", "Tripura", "Mizoram", "Manipur", "Nagaland", "Arunachal Pradesh"]
    districts = []
    for state in states:
        for i in range(1, np.random.randint(5, 15)):
            districts.append({"state": state, "district": f"{state} District {i}"})
            
    df_districts = pd.DataFrame(districts)
    df_districts['lat'] = np.random.uniform(22.0, 28.0, len(df_districts))
    df_districts['lon'] = np.random.uniform(89.0, 96.0, len(df_districts))
    
    records = []
    
    diseases = ["Acute Diarrhoeal Disease", "Cholera", "Typhoid", "Leptospirosis"]
    
    for _, row in df_districts.iterrows():
        for disease in diseases:
            # 8 weeks of historical data
            base_cases = int(np.random.gamma(shape=2, scale=2))
            
            # Determine risk roughly based on random factors for demo
            risk_val = np.random.rand()
            if risk_val > 0.85:
                risk_level = "HIGH"
                trend = np.random.randint(20, 60)
            elif risk_val > 0.6:
                risk_level = "MEDIUM"
                trend = np.random.randint(5, 20)
            else:
                risk_level = "LOW"
                trend = np.random.randint(-10, 5)
                
            current_cases = max(0, base_cases + np.random.randint(-2, 5))
            predicted_cases = max(0, int(current_cases * (1 + trend/100.0)))
            
            history = [max(0, current_cases - int(current_cases * np.random.rand())) for _ in range(7)]
            history.append(current_cases)
            
            records.append({
                "state": row["state"],
                "district": row["district"],
                "lat": row["lat"],
                "lon": row["lon"],
                "disease": disease,
                "current_cases": current_cases,
                "predicted_cases": predicted_cases,
                "historical_baseline": max(0, int(np.mean(history))),
                "trend_percentage": trend,
                "risk_level": risk_level,
                "precipitation": np.random.choice(["Normal", "Elevated", "High"]),
                "temperature": np.random.uniform(25, 35),
                "lai": np.random.uniform(1.0, 4.0),
                "history": history
            })
            
    return pd.DataFrame(records)

@st.cache_data
def get_risk_summary(df):
    total = len(df['district'].unique())
    high = len(df[df['risk_level'] == 'HIGH']['district'].unique())
    medium = len(df[df['risk_level'] == 'MEDIUM']['district'].unique())
    low = total - high - medium
    alerts = high
    return total, high, medium, low, alerts
"""

header_py = """import streamlit as st

def render_header():
    st.markdown(f'''
    <div class="header-container">
        <div style="display: flex; align-items: center;">
            <div class="header-logo">
                <span style="font-size: 32px; color: #0ea5e9;">🛡️</span>
                <div>
                    <h1 class="header-title">HealthSeers</h1>
                    <h2 class="header-subtitle">See the Risk. Stop the Outbreak.</h2>
                </div>
            </div>
            <div class="header-desc">
                AI-powered community health monitoring<br>
                and early warning system for<br>
                water-borne disease outbreaks.
            </div>
        </div>
        
        <div class="header-stages">
            <div class="stage-item">
                <span style="font-size: 20px; color: #3b82f6;">👥</span>
                <span>MONITOR</span>
            </div>
            <span>→</span>
            <div class="stage-item">
                <span style="font-size: 20px; color: #22c55e;">🧠</span>
                <span>PREDICT</span>
            </div>
            <span>→</span>
            <div class="stage-item">
                <span style="font-size: 20px; color: #ef4444;">⚠️</span>
                <span>WARN</span>
            </div>
            <span>→</span>
            <div class="stage-item">
                <span style="font-size: 20px; color: #8b5cf6;">🛡️</span>
                <span>PREVENT</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
"""

sidebar_py = """import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown('''
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="margin:0; color:#0ea5e9;">🛡️ HealthSeers</h2>
            <p style="margin:0; font-size: 14px; color:#94a3b8;">Early Warning System</p>
        </div>
        ''', unsafe_allow_html=True)
        
        pages = {
            "Overview": "⌂",
            "Risk Map": "◉",
            "District Analysis": "▣",
            "Alerts & Actions": "⚠️",
            "Disease Trends": "◔",
            "About / Methodology": "ⓘ"
        }
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Overview"
            
        for page_name, icon in pages.items():
            if st.button(f"{icon} {page_name}", key=page_name, use_container_width=True, 
                         type="primary" if st.session_state.current_page == page_name else "secondary"):
                st.session_state.current_page = page_name
                st.rerun()
                
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        st.markdown('''
        <div style="font-size: 12px; color: #94a3b8; border-top: 1px solid #334155; padding-top: 15px;">
            <b>SYSTEM STATUS</b><br>
            <span style="color: #22c55e;">●</span> AI ENGINE ONLINE<br><br>
            <b>DATA STATUS</b><br>
            <span style="color: #22c55e;">●</span> DATA AVAILABLE
            <br><br><br>
            SIH 2026<br>
            SIH25001
        </div>
        ''', unsafe_allow_html=True)
"""

cards_py = """import streamlit as st

def render_kpi_cards(total, high, medium, low, alerts):
    cols = st.columns(5)
    
    with cols[0]:
        st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-title">MONITORED DISTRICTS</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-subtitle">Districts</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown(f'''
        <div class="kpi-card" style="border-bottom: 4px solid #ef4444;">
            <div class="kpi-title">HIGH RISK</div>
            <div class="kpi-value risk-high">{high}</div>
            <div class="kpi-subtitle">Districts</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[2]:
        st.markdown(f'''
        <div class="kpi-card" style="border-bottom: 4px solid #f59e0b;">
            <div class="kpi-title">MEDIUM RISK</div>
            <div class="kpi-value risk-medium">{medium}</div>
            <div class="kpi-subtitle">Districts</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[3]:
        st.markdown(f'''
        <div class="kpi-card" style="border-bottom: 4px solid #10b981;">
            <div class="kpi-title">LOW RISK</div>
            <div class="kpi-value risk-low">{low}</div>
            <div class="kpi-subtitle">Districts</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[4]:
        st.markdown(f'''
        <div class="kpi-card" style="border-bottom: 4px solid #ef4444;">
            <div class="kpi-title">ACTIVE ALERTS</div>
            <div class="kpi-value risk-high">{alerts}</div>
            <div class="kpi-subtitle">Require attention</div>
        </div>
        ''', unsafe_allow_html=True)

def render_high_risk_list(df):
    st.markdown('<div class="generic-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">HIGH RISK AREAS</div>', unsafe_allow_html=True)
    
    high_risk_df = df[df['risk_level'] == 'HIGH'].sort_values(by='predicted_cases', ascending=False).head(5)
    
    if len(high_risk_df) == 0:
        st.info("No high risk areas detected.")
    else:
        for _, row in high_risk_df.iterrows():
            st.markdown(f'''
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #f1f5f9;">
                <div>
                    <div style="font-weight: 600; font-size: 14px; color: #0f172a;">{row['district']} ({row['state']})</div>
                    <div style="font-size: 12px; color: #64748b;">Predicted Cases: <b>{row['predicted_cases']}</b></div>
                    <div style="font-size: 12px; color: #64748b;">Disease: {row['disease']}</div>
                </div>
                <span class="badge-high">HIGH</span>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_lower_overview_cards(top_high_risk_district):
    cols = st.columns(4)
    
    if top_high_risk_district is None:
        dist_name = "N/A"
        pred_cases = 0
        trend = 0
    else:
        dist_name = top_high_risk_district['district']
        pred_cases = top_high_risk_district['predicted_cases']
        trend = top_high_risk_district['trend_percentage']
        
    with cols[0]:
        st.markdown(f'''
        <div class="generic-card alert-summary-card" style="height: 220px;">
            <div class="card-title" style="border-bottom-color: #fca5a5;">ALERT SUMMARY</div>
            <div style="color: #b91c1c; font-weight: bold; margin-bottom: 5px;">🔴 HIGH RISK OUTBREAK</div>
            <div style="font-weight: 600; margin-bottom: 10px;">{dist_name}</div>
            <p style="font-size: 13px; color: #7f1d1d; margin-bottom: 15px;">Disease activity is increasing. Predicted increase in cases next week.</p>
            <div style="font-size: 12px; color: #991b1b;">
                Predicted Cases: <b>{pred_cases}</b><br>
                Updated: Current analysis
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown('''
        <div class="generic-card" style="height: 220px;">
            <div class="card-title">TOP RISK FACTORS</div>
            <ul style="font-size: 13px; color: #334155; padding-left: 20px; margin-top: 10px;">
                <li style="margin-bottom: 8px;"><b>✓</b> Increase in predicted cases</li>
                <li style="margin-bottom: 8px;"><b>✓</b> Recent precipitation elevated</li>
                <li style="margin-bottom: 8px;"><b>✓</b> Cases above historical baseline</li>
                <li><b>✓</b> Abnormal trend detected</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[2]:
        st.markdown('''
        <div class="generic-card" style="height: 220px;">
            <div class="card-title">RECOMMENDED ACTIONS</div>
            <ul style="font-size: 13px; color: #334155; list-style-type: none; padding-left: 0; margin-top: 10px;">
                <li style="margin-bottom: 8px;">◉ Test local water sources</li>
                <li style="margin-bottom: 8px;">◉ Increase health surveillance</li>
                <li style="margin-bottom: 8px;">◉ Alert nearby health workers</li>
                <li>◉ Issue preventive community advisory</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
    with cols[3]:
        st.markdown(f'''
        <div class="generic-card" style="height: 220px; text-align: center;">
            <div class="card-title">CURRENT RISK LEVEL</div>
            <div style="font-size: 42px; font-weight: 800; color: #ef4444; margin: 10px 0;">HIGH</div>
            <div style="font-size: 16px; font-weight: 600;">{dist_name}</div>
            <div style="font-size: 13px; color: #64748b; margin-top: 10px;">
                Predicted Cases: <b>{pred_cases}</b><br>
                <span style="color: #ef4444;">↑ {trend}%</span> from previous week
            </div>
        </div>
        ''', unsafe_allow_html=True)
"""

charts_py = """import plotly.graph_objects as go
import streamlit as st

def render_disease_trend_chart(district_data):
    st.markdown('<div class="generic-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="card-title">DISEASE TREND ({district_data["district"]})</div>', unsafe_allow_html=True)
    
    history = district_data['history']
    predicted = district_data['predicted_cases']
    
    x_hist = [f"W{i+1}" for i in range(len(history))]
    x_pred = [f"W{len(history)}", f"W{len(history)+1}"]
    
    y_hist = history
    y_pred = [history[-1], predicted]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_hist, y=y_hist,
        mode='lines+markers',
        name='Historical Cases',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=x_pred, y=y_pred,
        mode='lines+markers',
        name='Predicted Cases',
        line=dict(color='#ef4444', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=250,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Weeks",
        yaxis_title="Cases",
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode="x unified"
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_env_charts():
    cols = st.columns(3)
    
    import numpy as np
    weeks = [f"W{i}" for i in range(1, 9)]
    
    with cols[0]:
        fig = go.Figure(go.Bar(x=weeks, y=np.random.uniform(10, 50, 8), marker_color='#3b82f6'))
        fig.update_layout(title="Weekly Precipitation (mm)", height=250, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with cols[1]:
        fig = go.Figure(go.Scatter(x=weeks, y=np.random.uniform(25, 35, 8), mode='lines+markers', marker_color='#f59e0b'))
        fig.update_layout(title="Weekly Temperature (°C)", height=250, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with cols[2]:
        fig = go.Figure(go.Scatter(x=weeks, y=np.random.uniform(1.5, 3.5, 8), mode='lines+markers', marker_color='#10b981'))
        fig.update_layout(title="Leaf Area Index (LAI)", height=250, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)
"""

map_py = """import streamlit as st
import pydeck as pdk
import pandas as pd

def render_risk_map(df):
    st.markdown('<div class="generic-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">COMMUNITY RISK MAP <span style="font-size:12px; font-weight:normal; color:#64748b; text-transform:none;">District-level predicted outbreak risk</span></div>', unsafe_allow_html=True)
    
    # Map colors
    color_map = {
        'HIGH': [239, 68, 68, 200],   # Red
        'MEDIUM': [245, 158, 11, 200], # Yellow/Orange
        'LOW': [16, 185, 129, 200]     # Green
    }
    
    df_map = df.copy()
    df_map['color'] = df_map['risk_level'].map(color_map)
    df_map['radius'] = df_map['risk_level'].map({'HIGH': 30000, 'MEDIUM': 20000, 'LOW': 15000})
    
    # Aggregate by district for map view (just taking first disease for demo if multiple exist)
    df_map = df_map.drop_duplicates(subset=['district'])
    
    layer = pdk.Layer(
        'ScatterplotLayer',
        df_map,
        get_position='[lon, lat]',
        get_color='color',
        get_radius='radius',
        pickable=True,
        auto_highlight=True
    )
    
    view_state = pdk.ViewState(
        latitude=25.0,
        longitude=92.0,
        zoom=5,
        pitch=0
    )
    
    tooltip = {
        "html": "<b>District:</b> {district}<br/>"
                "<b>State:</b> {state}<br/>"
                "<b>Disease:</b> {disease}<br/>"
                "<b>Current Cases:</b> {current_cases}<br/>"
                "<b>Predicted Cases:</b> {predicted_cases}<br/>"
                "<b>Risk:</b> <span style='color: white;'><b>{risk_level}</b></span><br/>"
                "<b>Trend:</b> {trend_percentage}%",
        "style": {
            "backgroundColor": "#1e293b",
            "color": "white"
        }
    }
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style='mapbox://styles/mapbox/light-v10'
    )
    
    st.pydeck_chart(r)
    
    # Legend
    st.markdown('''
    <div style="display: flex; gap: 15px; margin-top: 10px; font-size: 13px;">
        <div style="display: flex; align-items: center; gap: 5px;"><div style="width:12px; height:12px; border-radius:50%; background-color:#ef4444;"></div> HIGH RISK</div>
        <div style="display: flex; align-items: center; gap: 5px;"><div style="width:12px; height:12px; border-radius:50%; background-color:#f59e0b;"></div> MEDIUM RISK</div>
        <div style="display: flex; align-items: center; gap: 5px;"><div style="width:12px; height:12px; border-radius:50%; background-color:#10b981;"></div> LOW RISK</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
"""

app_py = """import streamlit as st
import pandas as pd

# Must be the first Streamlit command
st.set_page_config(
    page_title="HealthSeers",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load local modules
import os
from utils.data_loader import load_demo_data, get_risk_summary
from components.header import render_header
from components.sidebar import render_sidebar
from components.cards import render_kpi_cards, render_high_risk_list, render_lower_overview_cards
from components.charts import render_disease_trend_chart, render_env_charts
from components.map import render_risk_map

# Load custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

# Load Data
with st.spinner("Analyzing community health signals..."):
    df = load_demo_data()

# Render UI Shell
render_sidebar()

# Page Routing
current_page = st.session_state.get('current_page', 'Overview')

if current_page == 'Overview':
    render_header()
    
    st.markdown('<div style="display: flex; justify-content: space-between; align-items: center;">'
                '<h3 style="margin: 0;">HEALTHSEERS DASHBOARD <span style="font-size:16px; font-weight:normal; color:#64748b;">Community Health Monitoring & Early Warning</span></h3>'
                '<div style="font-size: 14px; font-weight: 600; color: #10b981;">● SYSTEM ACTIVE</div>'
                '</div><br>', unsafe_allow_html=True)
                
    total, high, medium, low, alerts = get_risk_summary(df)
    render_kpi_cards(total, high, medium, low, alerts)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Map and High Risk List / Chart
    col1, col2 = st.columns([6, 4])
    
    with col1:
        render_risk_map(df)
        
    with col2:
        render_high_risk_list(df)
        
        # Get top district for chart
        high_risk_df = df[df['risk_level'] == 'HIGH'].sort_values(by='predicted_cases', ascending=False)
        if len(high_risk_df) > 0:
            top_district = high_risk_df.iloc[0]
            render_disease_trend_chart(top_district)
        else:
            top_district = df.iloc[0]
            render_disease_trend_chart(top_district)
            
    # Lower Section
    st.markdown("<br>", unsafe_allow_html=True)
    render_lower_overview_cards(top_district if len(high_risk_df) > 0 else None)
    
    # System Architecture Strip
    st.markdown('''
    <div class="architecture-strip">
        <h4 style="margin-top: 0; margin-bottom: 20px; text-align: center; color: #1e293b;">SYSTEM ARCHITECTURE</h4>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">🛢️</div>
                <b>Raw Data</b><br><span style="color:#64748b;">Disease + Env</span>
            </div>
            <div>→</div>
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">⚙️</div>
                <b>Preprocessing</b><br><span style="color:#64748b;">Cleaning & Features</span>
            </div>
            <div>→</div>
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">📊</div>
                <b>Sequence</b><br><span style="color:#64748b;">Time-Series Prep</span>
            </div>
            <div>→</div>
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">🧠</div>
                <b>LSTM Model</b><br><span style="color:#64748b;">Next Week Prediction</span>
            </div>
            <div>→</div>
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">🎯</div>
                <b>Risk Engine</b><br><span style="color:#64748b;">Analysis</span>
            </div>
            <div>→</div>
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">🚦</div>
                <b>Risk Level</b><br><span style="color:#64748b;">Low/Medium/High</span>
            </div>
            <div>→</div>
            <div class="arch-stage">
                <div style="font-size: 30px; margin-bottom: 5px;">🔔</div>
                <b>Early Warning</b><br><span style="color:#64748b;">Alerts & Dashboard</span>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between;">
            <div style="flex: 1;">
                <b>TECH STACK:</b> &nbsp; 
                <span style="font-size: 13px; color: #475569;">Python | Pandas | NumPy | TensorFlow/Keras | Scikit-learn | Streamlit | Plotly | PyDeck</span>
            </div>
            <div style="font-size: 13px;">
                <b>IDEAL IMPACT:</b> &nbsp;
                <span style="color: #0ea5e9; font-weight: 600;">DETECT EARLY. WARN FASTER. PREVENT OUTBREAKS.</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
elif current_page == 'District Analysis':
    st.title("DISTRICT ANALYSIS")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("STATE", df['state'].unique())
    with col2:
        st.selectbox("DISTRICT", df['district'].unique())
    with col3:
        st.selectbox("DISEASE", df['disease'].unique())
        
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Get arbitrary district for demo
    district_data = df.iloc[0]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CURRENT CASES", district_data['current_cases'])
    c2.metric("PREDICTED CASES", district_data['predicted_cases'])
    c3.metric("HISTORICAL BASELINE", district_data['historical_baseline'])
    c4.metric("TREND", f"↑ {district_data['trend_percentage']}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown(f'''
        <div class="generic-card">
            <div class="card-title">CURRENT DISTRICT RISK</div>
            <h1 class="risk-high">HIGH</h1>
            <h3>{district_data['district']}</h3>
            
            <h5 style="margin-top: 20px;">Why?</h5>
            <ul>
                <li>Cases increasing rapidly</li>
                <li>Precipitation elevated above normal</li>
                <li>Exceeds historical baseline for this week</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col_r:
        render_disease_trend_chart(district_data)
        
    st.markdown("### ENVIRONMENTAL SIGNALS")
    render_env_charts()

elif current_page == 'Risk Map':
    st.title("COMMUNITY RISK MAP")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Disease", ["All"] + list(df['disease'].unique()))
    with col2:
        st.selectbox("State", ["All"] + list(df['state'].unique()))
    with col3:
        st.selectbox("Risk Level", ["All", "HIGH", "MEDIUM", "LOW"])
        
    st.markdown("<br>", unsafe_allow_html=True)
    render_risk_map(df)

elif current_page == 'Alerts & Actions':
    st.title("ACTIVE EARLY WARNINGS")
    
    alerts_df = df[df['risk_level'] == 'HIGH'].copy()
    
    st.dataframe(
        alerts_df[['risk_level', 'district', 'state', 'disease', 'current_cases', 'predicted_cases', 'trend_percentage']],
        use_container_width=True,
        hide_index=True
    )

elif current_page == 'Disease Trends':
    st.title("DISEASE TRENDS")
    st.info("Analytics view. Select parameters below to explore historical and predicted data.")
    
    district_data = df.iloc[0]
    render_disease_trend_chart(district_data)

elif current_page == 'About / Methodology':
    st.title("HOW HEALTHSEERS WORKS")
    
    st.markdown('''
    ### Methodology
    
    HealthSeers uses a robust data pipeline and Deep Learning to provide early warnings.
    
    1. **DATA COLLECTION**: Historical disease data and environmental indicators.
    2. **DATA PROCESSING**: Cleaning, filtering, and feature engineering.
    3. **FEATURE PREPARATION**: Formatting data for sequential models.
    4. **TIME-SERIES SEQUENCES**: Creating sliding windows of historical context.
    5. **LSTM MODEL**: Predicting next week's cases based on sequence patterns.
    6. **RISK ENGINE**: Combining case predictions with environmental vulnerability.
    7. **RISK LEVEL**: Outputting actionable LOW / MEDIUM / HIGH indicators.
    8. **EXPLAINABLE WARNING**: Providing transparent reasons for the risk.
    9. **PREVENTIVE ACTION**: Suggesting public-health interventions.
    ''')
    
# Footer
st.markdown('''
<div style="background-color: #0f172a; color: white; padding: 20px; text-align: center; margin-top: 50px; border-radius: 8px;">
    <h3 style="margin:0; color: #0ea5e9;">HealthSeers</h3>
    <p style="margin:5px 0 0 0;">See the Risk. Stop the Outbreak.</p>
    <p style="font-size: 12px; color: #94a3b8; margin-top: 10px;">Community-level early warning for proactive public-health action.</p>
</div>
''', unsafe_allow_html=True)
"""

if __name__ == "__main__":
    base_dir = r"c:\Users\ANKAN MONDAL\sih\HealthSeers\ui"
    
    create_file(os.path.join(base_dir, "requirements.txt"), requirements)
    create_file(os.path.join(base_dir, "assets", "style.css"), style_css)
    create_file(os.path.join(base_dir, "utils", "data_loader.py"), data_loader_py)
    create_file(os.path.join(base_dir, "components", "header.py"), header_py)
    create_file(os.path.join(base_dir, "components", "sidebar.py"), sidebar_py)
    create_file(os.path.join(base_dir, "components", "cards.py"), cards_py)
    create_file(os.path.join(base_dir, "components", "charts.py"), charts_py)
    create_file(os.path.join(base_dir, "components", "map.py"), map_py)
    create_file(os.path.join(base_dir, "app.py"), app_py)
    
    print("Files generated successfully.")
