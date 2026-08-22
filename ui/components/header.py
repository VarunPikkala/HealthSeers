import streamlit as st


def render_header():
    is_dark = st.session_state.get("theme") == "dark"
    st.markdown("""
    <div class="top-header">
      <div class="brand-lockup"><div class="shield">+</div><div><div class="brand-name">HealthSeers</div><div class="tagline">See the Risk. Stop the Outbreak.</div></div></div>
      <div class="header-copy">AI-powered community monitoring<br>for water-borne disease early warnings.</div>
      <div class="pipeline"><span>MONITOR</span><b>-></b><span>PREDICT</span><b>-></b><span>WARN</span><b>-></b><span>PREVENT</span></div>
    </div>
    """, unsafe_allow_html=True)
    toggle_label = "LIGHT  |  DARK" if is_dark else "LIGHT  |  DARK"
    if st.button(("☀ " if not is_dark else "🌙 ") + toggle_label, key="theme_toggle", help="Switch dashboard theme"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()
