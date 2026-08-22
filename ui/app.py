import os

import pandas as pd
import streamlit as st

from components.cards import render_high_risk_list, render_kpi_cards, render_lower_overview_cards
from components.charts import render_disease_trend_chart, render_env_charts
from components.header import render_header
from components.map import render_risk_map
from components.sidebar import render_sidebar
from utils.data_loader import filter_data, get_high_risk_districts, get_risk_summary, load_data
from utils.theme import get_theme, initialize_theme, theme_css

st.set_page_config(page_title="HealthSeers", page_icon="+", layout="wide", initial_sidebar_state="expanded")


def load_css():
    path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    with open(path, encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)


def page_heading(title, subtitle):
    st.markdown(f'<div class="page-heading"><div><div class="eyebrow">HEALTHSEERS DASHBOARD</div><h1>{title}</h1><p>{subtitle}</p></div><span class="active-pill"><i></i> SYSTEM ACTIVE</span></div>', unsafe_allow_html=True)


def select_filters(df, key_prefix="filter", include_risk=False):
    columns = st.columns(4 if include_risk else 3)
    states = ["All"] + sorted(df.state_ut.dropna().unique().tolist())
    with columns[0]:
        state = st.selectbox("STATE", states, key=f"{key_prefix}_state")
    state_df = filter_data(df, state=state)
    districts = ["All"] + sorted(state_df.district.dropna().unique().tolist())
    with columns[1]:
        district = st.selectbox("DISTRICT", districts, key=f"{key_prefix}_district")
    diseases = ["All"] + sorted(df.disease.dropna().unique().tolist())
    with columns[2]:
        disease = st.selectbox("DISEASE", diseases, key=f"{key_prefix}_disease")
    risk = "All"
    if include_risk:
        with columns[3]:
            risk = st.selectbox("RISK LEVEL", ["All", "HIGH", "MEDIUM", "LOW"], key=f"{key_prefix}_risk")
    return filter_data(df, state=state, district=district, disease=disease, risk=risk)


def overview(df):
    page_heading("Community health monitoring", "Early warning signals for water-borne disease outbreaks across Northeast India.")
    total, high, medium, low, alerts = get_risk_summary(df)
    render_kpi_cards(total, high, medium, low, alerts)
    st.markdown('<div class="demo-note"><b>DEMO MODE</b> Simulated predictions are shown for presentation. The same interface accepts processed data and model output.</div>', unsafe_allow_html=True)
    map_column, list_column = st.columns([1.55, 1])
    high_risk = get_high_risk_districts(df)
    with map_column:
        render_risk_map(df)
    with list_column:
        render_high_risk_list(high_risk)
        if not high_risk.empty:
            render_disease_trend_chart(high_risk.iloc[0], "DISEASE TREND")
    top = high_risk.iloc[0] if not high_risk.empty else df.iloc[0]
    render_lower_overview_cards(top)
    architecture()


def district_analysis(df):
    page_heading("District analysis", "Inspect the signals behind a community-level risk score.")
    selected = select_filters(df, "district")
    row = selected.iloc[0] if not selected.empty else df.iloc[0]
    metrics = st.columns(4)
    for column, label, value in zip(metrics, ["CURRENT CASES", "PREDICTED CASES", "HISTORICAL BASELINE", "TREND"], [row.current_cases, row.predicted_cases, row.historical_baseline, f"+{row.trend_percentage}%"]):
        column.metric(label, value)
    left, right = st.columns([0.8, 1.2])
    with left:
        st.markdown(f'<div class="panel explanation"><div class="panel-heading">CURRENT DISTRICT RISK</div><div class="big-risk {row.risk_level.lower()}">{row.risk_level}</div><h3>{row.district}</h3><p>Cases increasing<br>Precipitation elevated<br>Above historical baseline</p></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="panel-heading">CASE TRAJECTORY <small>Historical and next-week forecast</small></div>', unsafe_allow_html=True)
        render_disease_trend_chart(row, "CASE TRAJECTORY")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">ENVIRONMENTAL SIGNALS</div>', unsafe_allow_html=True)
    render_env_charts(row)
    st.markdown('<div class="panel explanation"><div class="panel-heading">WHY IS THIS DISTRICT AT RISK?</div><p>HealthSeers detected elevated signals across recent disease activity and environmental conditions.</p><b>Recommended actions</b><p>→ Increase local surveillance<br>→ Test local water sources<br>→ Monitor nearby communities<br>→ Issue preventive advisory</p></div>', unsafe_allow_html=True)


def risk_map_page(df):
    page_heading("Community risk map", "Explore district-level predicted outbreak risk.")
    selected = select_filters(df, "map", True)
    render_risk_map(selected if not selected.empty else df)


def alerts_page(df):
    page_heading("Active early warnings", "Prioritized signals for proactive public-health action.")
    selected = select_filters(df, "alerts", True)
    alerts = selected[selected.risk_level.isin(["HIGH", "MEDIUM"])].sort_values(["risk_level", "predicted_cases"], ascending=[True, False])
    display = alerts[["risk_level", "district", "state_ut", "disease", "current_cases", "predicted_cases", "trend_percentage"]].rename(columns={"risk_level": "Risk", "district": "District", "state_ut": "State", "disease": "Disease", "current_cases": "Current Cases", "predicted_cases": "Predicted Cases", "trend_percentage": "Trend %"})
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.info("Recommended response: monitor local signals, verify water sources, and coordinate with nearby health workers.")


def trends_page(df):
    page_heading("Disease trends", "Compare historical activity with model-ready environmental signals.")
    selected = select_filters(df, "trends")
    row = selected.iloc[0] if not selected.empty else df.iloc[0]
    left, right = st.columns(2)
    with left:
        render_disease_trend_chart(row, "DISEASE CASES OVER TIME")
    with right:
        render_env_charts(row)
    summary = df.groupby("state_ut", as_index=False)["current_cases"].sum().sort_values("current_cases", ascending=False)
    st.bar_chart(summary.set_index("state_ut"), height=260)


def methodology():
    page_heading("How HealthSeers works", "A transparent path from community signals to preventive action.")
    steps = [("01", "DATA COLLECTION", "Disease, weather, geography"), ("02", "PREPROCESSING", "Cleaning and feature preparation"), ("03", "SEQUENCES", "Six to eight week windows"), ("04", "LSTM MODEL", "Next-week case prediction"), ("05", "RISK ENGINE", "Prediction plus signals"), ("06", "EARLY WARNING", "Explainable actions")]
    st.markdown('<div class="method-grid">' + ''.join(f'<div class="method-step"><span>{number}</span><b>{title}</b><small>{description}</small></div>' for number, title, description in steps) + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel methodology-copy"><h3>Designed for public-health monitoring</h3><p>HealthSeers is a community-level early warning prototype, not an individual medical diagnosis tool. It combines historical disease cases and environmental indicators to help teams investigate emerging risk earlier.</p><div class="impact"><b>DETECT EARLY</b><b>WARN FASTER</b><b>PREVENT PROACTIVELY</b></div></div>', unsafe_allow_html=True)


def architecture():
    st.markdown('<div class="architecture"><div class="section-title">SYSTEM ARCHITECTURE</div><div class="architecture-flow">' + ''.join(f'<span><b>{title}</b><small>{description}</small></span>' + ('<i>→</i>' if index < 5 else '') for index, (title, description) in enumerate([("RAW DATA", "Disease + environment"), ("PREPROCESSING", "Cleaning + features"), ("SEQUENCES", "Time-series windows"), ("LSTM", "Next-week prediction"), ("RISK ENGINE", "Signals + prediction"), ("WARNING", "Alerts + actions")])) + '</div><div class="tech-strip"><b>TECH STACK</b> Python · Pandas · NumPy · TensorFlow · Keras · Streamlit · Plotly · PyDeck</div></div>', unsafe_allow_html=True)


initialize_theme()
load_css()
st.markdown(theme_css(get_theme()), unsafe_allow_html=True)
with st.spinner("Analyzing community health signals..."):
    data = load_data()
render_sidebar()
page = st.session_state.get("current_page", "Overview")
render_header()
if page == "Overview":
    overview(data)
elif page == "District Analysis":
    district_analysis(data)
elif page == "Risk Map":
    risk_map_page(data)
elif page == "Alerts & Actions":
    alerts_page(data)
elif page == "Disease Trends":
    trends_page(data)
else:
    methodology()

st.markdown('<footer><b>HealthSeers</b><br><span>See the Risk. Stop the Outbreak.</span><small>Community-level early warning for proactive public-health action.</small></footer>', unsafe_allow_html=True)
