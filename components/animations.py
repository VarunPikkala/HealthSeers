import streamlit as st
import time


def run_analysis():

    st.markdown(
        """
        <div class="glass-card cyan-glow">

            <div class="metric-label">
                ◉ AI RISK ENGINE
            </div>

            <div style="
                color:#64748B;
                font-size:12px;
                margin-top:6px;
            ">
                Processing community signals
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    status = st.empty()
    progress = st.progress(0)

    steps = [
        ("COLLECTING COMMUNITY SIGNALS", 15),
        ("ANALYZING DISEASE TRENDS", 30),
        ("CHECKING WATER QUALITY", 48),
        ("ANALYZING WEATHER SIGNALS", 65),
        ("DETECTING ANOMALIES", 82),
        ("CALCULATING OUTBREAK RISK", 95),
        ("ANALYSIS COMPLETE", 100),
    ]

    for message, percentage in steps:

        status.markdown(
            f"""
            <div style="
                color:#22D3EE;
                font-size:13px;
                font-weight:700;
                letter-spacing:1px;
                margin-top:10px;
            ">
                ◉ {message}
            </div>
            """,
            unsafe_allow_html=True,
        )

        progress.progress(percentage)

        time.sleep(0.4)

    return True