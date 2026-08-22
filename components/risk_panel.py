import streamlit as st


def render_risk_panel(prediction):

    score = prediction["risk_score"]
    level = prediction["risk_level"]

    if level == "HIGH":
        risk_class = "risk-high"
        icon = "🔴"

    elif level == "MEDIUM":
        risk_class = "risk-medium"
        icon = "🟡"

    else:
        risk_class = "risk-low"
        icon = "🟢"

    # Risk card
    st.markdown(
        f'<div class="glass-card cyan-glow fade-in">'
        f'<div class="metric-label">AI OUTBREAK RISK</div>'
        f'<div class="risk-score">{score}%</div>'
        f'<div class="{risk_class}">{icon} {level} RISK</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Risk Factors")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"📈 Cases: **+{prediction['cases_change']}%**"
        )

        st.write(
            f"💧 Water quality: **{prediction['water_quality']}**"
        )

    with col2:
        st.write(
            f"🌧️ Rainfall: **{prediction['rainfall']}**"
        )

        flood = (
            "DETECTED"
            if prediction["flooding"]
            else "NOT DETECTED"
        )

        st.write(
            f"🌊 Flooding: **{flood}**"
        )