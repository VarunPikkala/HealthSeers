import streamlit as st


def render_metrics(metrics):

    cols = st.columns(4)

    for i, metric in enumerate(metrics):

        with cols[i]:

            st.markdown(
                f'<div class="glass-card cyan-glow">'
                f'<div class="metric-label">{metric["label"]}</div>'
                f'<div class="metric-value">{metric["value"]}</div>'
                f'<div style="color:#64748B;font-size:11px;margin-top:6px;">'
                f'{metric["description"]}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )