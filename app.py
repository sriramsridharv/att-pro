import streamlit as st
from dashboard.home import show_dashboard

st.set_page_config(
    page_title="ATT Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📈 ATT Pro")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Scanner",
        "Indicators",
        "Portfolio",
        "Reports",
        "Settings"
    ]
)

if page == "Dashboard":
    show_dashboard()

elif page == "Scanner":
    st.title("🔍 Scanner")
    st.info("Coming Soon")

elif page == "Indicators":
    st.title("📊 Indicators")
    st.info("Coming Soon")

elif page == "Portfolio":
    st.title("💼 Portfolio")
    st.info("Coming Soon")

elif page == "Reports":
    st.title("📄 Reports")
    st.info("Coming Soon")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.info("Coming Soon")