import streamlit as st


def render_header():

    left, right = st.columns([5, 1])

    with left:
        st.markdown(
            '<div class="brand">🩺 HEALTH<span class="brand-accent">SEERS</span></div>'
            '<div class="subtitle">Community Health Intelligence Platform '
            '· See the Risk. Stop the Outbreak.</div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            '<div style="text-align:right;">'
            '<div class="system-status">● SYSTEM ONLINE</div>'
            '<div style="color:#64748B;font-size:11px;margin-top:5px;">'
            'MONITORING ACTIVE'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.divider()