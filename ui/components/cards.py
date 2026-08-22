import html
import streamlit as st


def _safe(value):
    return html.escape(str(value))


def render_kpi_cards(total, high, medium, low, alerts):
    cards = [("MONITORED DISTRICTS", total, "Districts", "teal"), ("HIGH RISK", high, "Districts", "high"), ("MEDIUM RISK", medium, "Districts", "medium"), ("LOW RISK", low, "Districts", "low"), ("ACTIVE ALERTS", alerts, "Require attention", "high")]
    columns = st.columns(5)
    for column, (title, value, subtext, color) in zip(columns, cards):
        with column:
            st.markdown(f'<div class="kpi-card {color}"><div class="kpi-label">{title}</div><div class="kpi-number">{value}</div><div class="kpi-subtext">{subtext}</div></div>', unsafe_allow_html=True)


def render_high_risk_list(df):
    st.markdown('<div class="panel"><div class="panel-heading"><span>HIGH RISK AREAS</span><small>Priority districts</small></div>', unsafe_allow_html=True)
    for _, row in df.iterrows():
        st.markdown(f'<div class="risk-row"><div><strong>{_safe(row.district)}</strong><small>{_safe(row.state_ut)} · {row.predicted_cases} predicted cases</small></div><span class="badge badge-high">HIGH</span></div>', unsafe_allow_html=True)
    if df.empty:
        st.info("No high-risk districts match the current filters.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_lower_overview_cards(row):
    name = _safe(row.district) if row is not None else "No district selected"
    predicted = row.predicted_cases if row is not None else 0
    trend = row.trend_percentage if row is not None else 0
    columns = st.columns(4)
    contents = [
        f'<div class="panel alert-panel"><div class="panel-heading">ALERT SUMMARY</div><div class="alert-title">HIGH RISK</div><strong>{name}</strong><p>Disease activity is increasing above the historical baseline.</p><small>Predicted cases <b>{predicted}</b> · Current analysis</small></div>',
        '<div class="panel"><div class="panel-heading">TOP RISK FACTORS</div><ul class="clean-list"><li>Increase in predicted cases</li><li>Recent precipitation elevated</li><li>Cases above baseline</li><li>Abnormal trend detected</li></ul></div>',
        '<div class="panel"><div class="panel-heading">RECOMMENDED ACTIONS</div><ul class="clean-list actions"><li>Test local water sources</li><li>Increase health surveillance</li><li>Alert nearby health workers</li><li>Issue community advisory</li></ul></div>',
        f'<div class="panel current-risk"><div class="panel-heading">CURRENT RISK LEVEL</div><div class="big-risk">HIGH</div><strong>{name}</strong><small>Predicted cases <b>{predicted}</b><br><em>+{trend}%</em> from previous week</small></div>',
    ]
    for column, content in zip(columns, contents):
        with column:
            st.markdown(content, unsafe_allow_html=True)
