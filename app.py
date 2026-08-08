import streamlit as st
from dashboard.home import show_dashboard
from dashboard.scanner import show_scanner
from dashboard.indicators import show_indicators
from dashboard.portfolio import show_portfolio
from dashboard.reports import show_reports
from dashboard.settings import show_settings

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
    show_scanner()

elif page == "Indicators":
    show_indicators()

elif page == "Portfolio":
    show_portfolio()

elif page == "Reports":
    show_reports()

elif page == "Settings":
    show_settings()