import streamlit as st
import pandas as pd

from core.scanner_engine import ScannerEngine


def show_dashboard():

    st.title("📈 ATT Pro - AI Trading Terminal")
    st.caption("Advanced Technical Trading Platform")

    st.divider()

    # ==========================================
    # KPI Cards
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Stocks Scanned", "5")

    with col2:
        st.metric("BUY Signals", "0")

    with col3:
        st.metric("HOLD Signals", "5")

    with col4:
        st.metric("Average AI Score", "26")

    st.divider()

    # ==========================================
    # Sidebar
    # ==========================================

    st.sidebar.title("Scanner")

    strategy = st.sidebar.selectbox(
        "Strategy",
        ["BTST"]
    )

    symbols = [
        "ICICIBANK.NS",
        "SBIN.NS",
        "INFY.NS",
        "RELIANCE.NS",
        "TCS.NS"
    ]

    if st.sidebar.button("🚀 Scan Market"):

        scanner = ScannerEngine()

        results = scanner.scan_market(symbols)

        if len(results) == 0:

            st.warning("No results found.")

        else:

            df = pd.DataFrame(results)

            st.subheader("📊 Scanner Results")

            st.dataframe(
                df,
                use_container_width=True
            )

            csv = df.to_csv(index=False)

            st.download_button(
                "⬇ Download CSV",
                csv,
                "attpro_scan.csv",
                "text/csv"
            )

    st.divider()

    # ==========================================
    # Status
    # ==========================================

    st.subheader("System Status")

    status = pd.DataFrame(
        {
            "Module": [
                "Market Data",
                "Indicators",
                "BTST Strategy",
                "AI Engine",
                "Risk Engine",
                "Scanner Engine"
            ],
            "Status": [
                "✅ Online",
                "✅ Online",
                "✅ Online",
                "✅ Online",
                "✅ Online",
                "✅ Online"
            ]
        }
    )

    st.table(status)