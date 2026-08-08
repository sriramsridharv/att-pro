import streamlit as st
import pandas as pd

from core.scanner_engine import ScannerEngine


def format_conditions(conditions):
    """
    Convert scanner conditions into a Streamlit-friendly string.
    """

    if not conditions:
        return "None"

    formatted = []

    for condition, passed in conditions:
        if bool(passed):
            formatted.append(f"{condition}: ✅")
        else:
            formatted.append(f"{condition}: ❌")

    return " | ".join(formatted)


def show_dashboard():

    st.title("📈 ATT Pro - AI Trading Terminal")
    st.caption("Advanced Technical Trading Platform")

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

    # ==========================================
    # Scanner
    # ==========================================

    if st.sidebar.button("🚀 Scan Market"):

        scanner = ScannerEngine()

        with st.spinner("Scanning market..."):

            results = scanner.scan_market(symbols)

        if not results:

            st.warning("No results found.")

        else:

            # ==========================================
            # Convert results for dashboard
            # ==========================================

            display_results = []

            for stock in results:

                row = stock.copy()

                # Convert Conditions list/tuples
                # into Streamlit-safe text
                row["Conditions"] = format_conditions(
                    row.get("Conditions", [])
                )

                # Convert Reasons list into text
                reasons = row.get("Reasons", [])

                if reasons:
                    row["Reasons"] = ", ".join(
                        str(reason) for reason in reasons
                    )
                else:
                    row["Reasons"] = "None"

                display_results.append(row)

            df = pd.DataFrame(display_results)

            # ==========================================
            # KPI Calculations
            # ==========================================

            total_stocks = len(df)

            buy_count = 0

            if "Signal" in df.columns:
                buy_count = int(
                    (df["Signal"] == "BUY").sum()
                )

            hold_count = 0

            if "Signal" in df.columns:
                hold_count = int(
                    (df["Signal"] == "HOLD").sum()
                )

            average_ai = 0

            if "AI Score" in df.columns and total_stocks > 0:
                average_ai = round(
                    pd.to_numeric(
                        df["AI Score"],
                        errors="coerce"
                    ).mean()
                )

            # ==========================================
            # KPI Cards
            # ==========================================

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Stocks Scanned",
                    total_stocks
                )

            with col2:
                st.metric(
                    "BUY Signals",
                    buy_count
                )

            with col3:
                st.metric(
                    "HOLD Signals",
                    hold_count
                )

            with col4:
                st.metric(
                    "Average AI Score",
                    average_ai
                )

            st.divider()

            # ==========================================
            # Scanner Results
            # ==========================================

            st.subheader("📊 Scanner Results")

            # Sort by AI Score
            if "AI Score" in df.columns:

                df = df.sort_values(
                    by="AI Score",
                    ascending=False
                )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # ==========================================
            # Download CSV
            # ==========================================

            csv = df.to_csv(index=False)

            st.download_button(
                "⬇ Download CSV",
                csv,
                "attpro_scan.csv",
                "text/csv"
            )

    else:

        # ==========================================
        # Initial KPI Cards
        # ==========================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Stocks Scanned", "0")

        with col2:
            st.metric("BUY Signals", "0")

        with col3:
            st.metric("HOLD Signals", "0")

        with col4:
            st.metric("Average AI Score", "0")

        st.info(
            "Select a strategy and click "
            "**🚀 Scan Market** to begin."
        )

    st.divider()

    # ==========================================
    # System Status
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