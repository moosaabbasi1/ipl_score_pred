"""
app.py  —  IPL Score Predictor · Main Entry Point
Run: streamlit run app.py
"""
import streamlit as st

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="IPL Score Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ────────────────────────────────────────────────────────────────
from utils import load_css
from page_views import home, predictor, analytics, team_stats, about

# ── Load CSS ───────────────────────────────────────────────────────────────
load_css()

# ── Session state: current page ────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── Sidebar Navigation ─────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">🏏 IPL PREDICTOR</div>
    <div class="sidebar-subtitle">AI · Cricket · Intelligence</div>
    <hr class="nav-divider">
    """, unsafe_allow_html=True)

    # Navigation items: (label, icon, page_key)
    NAV_ITEMS = [
        ("🏠  Home",             "Home"),
        ("🎯  Score Predictor",  "Predict"),
        ("📊  Analytics",        "Analytics"),
        ("⚔️  Team & Players",   "Teams"),
        ("ℹ️  About & Model",    "About"),
    ]

    st.markdown('<div style="margin-bottom:0.3rem; font-family:\'Rajdhani\',sans-serif; font-size:0.7rem; color:#3a5276; letter-spacing:0.15em; text-transform:uppercase;">Navigation</div>', unsafe_allow_html=True)

    for label, key in NAV_ITEMS:
        # Highlight active page with custom CSS wrapper
        is_active = st.session_state.page == key
        wrapper_class = "nav-active" if is_active else ""
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)

    # Current page indicator
    st.markdown(f"""
    <div style="text-align:center; padding:0.5rem 0;">
        <span class="badge">{st.session_state.page}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="position:absolute; bottom:1.5rem; left:0; right:0; text-align:center; opacity:0.3;">
        <div style="font-family:'Rajdhani',sans-serif; font-size:0.7rem; color:#4a6fa5;
                    letter-spacing:0.1em; text-transform:uppercase;">
            Streamlit · TensorFlow<br>IPL 2008–2017 Data
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Page Router ────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Home":
    home.show()
elif page == "Predict":
    predictor.show()
elif page == "Analytics":
    analytics.show()
elif page == "Teams":
    team_stats.show()
elif page == "About":
    about.show()