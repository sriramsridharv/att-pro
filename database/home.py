import streamlit as st

def show_dashboard():
    """Display the ATT Pro Home Dashboard."""

    st.title("📈 ATT Pro")
    st.caption("Advanced Trading Terminal Pro")

    st.divider()

    st.subheader("📊 Market Overview")

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

    st.subheader("⭐ AI Trade Opportunities")

    st.info("No trading opportunities available yet.")

    st.divider()

    st.subheader("🔍 Scanner Status")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success("BTST Scanner")

    with c2:
        st.warning("Swing Scanner")

    with c3:
        st.error("Intraday Scanner")

    st.divider()

    st.subheader("💼 Portfolio")

    st.write("Portfolio module coming soon.")

    st.divider()

    st.subheader("📄 Reports")

    st.write("Performance reports coming soon.")
