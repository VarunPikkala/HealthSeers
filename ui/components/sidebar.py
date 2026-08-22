import streamlit as st


def render_sidebar():
    pages = {"Overview": "01", "Risk Map": "02", "District Analysis": "03", "Alerts & Actions": "04", "Disease Trends": "05", "About / Methodology": "06"}
    with st.sidebar:
        st.markdown('<div class="side-brand"><div class="side-mark">+</div><div><strong>HealthSeers</strong><small>Early Warning System</small></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="side-label">WORKSPACE</div>', unsafe_allow_html=True)
        current = st.session_state.get("current_page", "Overview")
        for page, number in pages.items():
            if st.button(f"{number}  {page}", key=f"nav_{page}", use_container_width=True, type="primary" if current == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()
        st.markdown('<div class="side-status"><div class="side-label">SYSTEM STATUS</div><div class="status-line"><i></i> AI ENGINE ONLINE</div><div class="side-label">DATA STATUS</div><div class="status-line"><i></i> DATA AVAILABLE</div></div><div class="side-footer">SIH 2026<br><b>SIH25001</b></div>', unsafe_allow_html=True)
