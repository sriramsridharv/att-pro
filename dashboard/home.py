import streamlit as st


def show_dashboard():

    st.title("📈 ATT Pro")

    st.subheader("Advanced Trading Terminal Pro")

    st.divider()

    st.header("📊 Market Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("NIFTY 50", "--")

    with col2:
        st.metric("BANK NIFTY", "--")

    with col3:
        st.metric("SENSEX", "--")

    with col4:
        st.metric("INDIA VIX", "--")

    st.divider()

    st.header("⭐ AI Trade Opportunities")

    st.info("No trading opportunities available yet.")

    st.divider()

    st.header("🔍 Scanner Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("BTST Scanner")

    with col2:
        st.warning("Swing Scanner")

    with col3:
        st.error("Intraday Scanner")

    st.divider()

    st.header("💼 Portfolio")

    st.write("Portfolio module coming soon.")
