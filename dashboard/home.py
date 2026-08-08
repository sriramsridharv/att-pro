import streamlit as st
import pandas as pd

from core.scanner_engine import ScannerEngine


def format_conditions(conditions):
    """
    Convert Conditions into a simple text string
    that Streamlit/PyArrow can safely display.
    """

    if conditions is None:
        return "None"

    if not isinstance(conditions, (list, tuple)):
        return str(conditions)

    formatted = []

    for item in conditions:

        if isinstance(item, (list, tuple)) and len(item) >= 2:

            condition = str(item[0])
            passed = bool(item[1])

            status = "✅" if passed else "❌"

            formatted.append(
                f"{condition}: {status}"
            )

        else:
            formatted.append(str(item))

    return " | ".join(formatted)


def format_reasons(reasons):
    """
    Convert Reasons list into a simple string.
    """

    if reasons is None:
        return "None"

    if isinstance(reasons, (list, tuple)):

        if len(reasons) == 0:
            return "None"

        return ", ".join(
            str(reason)
            for reason in reasons
        )

    return str(reasons)


def make_streamlit_safe(results):
    """
    Convert scanner results into a DataFrame
    containing only Streamlit/PyArrow-safe values.
    """

    display_results = []

    for stock in results:

        row = {}

        for key, value in stock.items():

            # ------------------------------------------
            # Conditions
            # ------------------------------------------

            if key.lower() == "conditions":

                row[key] = format_conditions(value)

            # ------------------------------------------
            # Reasons
            # ------------------------------------------

            elif key.lower() == "reasons":

                row[key] = format_reasons(value)

            # ------------------------------------------
            # Lists / tuples / dictionaries
            # ------------------------------------------

            elif isinstance(value, (list, tuple, dict)):

                row[key] = str(value)

            # ------------------------------------------
            # Everything else
            # ------------------------------------------

            else:

                row[key] = value

        display_results.append(row)

    return pd.DataFrame(display_results)


def show_dashboard():

    st.title("📈 ATT Pro - AI Trading Terminal")

    st.caption(
        "Advanced Technical Trading Platform"
    )

    st.divider()

    # ==================================================
    # SIDEBAR
    # ==================================================

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

    # ==================================================
    # SCAN MARKET
    # ==================================================

    if st.sidebar.button("🚀 Scan Market"):

        scanner = ScannerEngine()

        with st.spinner(
            "Scanning market and calculating AI scores..."
        ):

            results = scanner.scan_market(symbols)

        # ==============================================
        # NO RESULTS
        # ==============================================

        if not results:

            st.warning(
                "No trading opportunities found."
            )

        else:

            # ==========================================
            # SAFE DATAFRAME
            # ==========================================

            df = make_streamlit_safe(results)

            # ==========================================
            # KPI CALCULATIONS
            # ==========================================

            total_stocks = len(df)

            buy_count = 0
            hold_count = 0
            average_ai = 0

            if "Signal" in df.columns:

                buy_count = int(
                    (
                        df["Signal"].astype(str)
                        .str.upper()
                        == "BUY"
                    ).sum()
                )

                hold_count = int(
                    (
                        df["Signal"].astype(str)
                        .str.upper()
                        == "HOLD"
                    ).sum()
                )

            if "AI Score" in df.columns:

                ai_scores = pd.to_numeric(
                    df["AI Score"],
                    errors="coerce"
                )

                if not ai_scores.empty:

                    average_ai = round(
                        ai_scores.mean()
                    )

            # ==========================================
            # KPI CARDS
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
            # RESULTS
            # ==========================================

            st.subheader(
                "📊 ATT Pro Scanner Results"
            )

            # Sort by AI Score

            if "AI Score" in df.columns:

                df = df.sort_values(
                    by="AI Score",
                    ascending=False
                )

            # ==========================================
            # FINAL SAFETY CHECK
            # ==========================================

            # Convert any remaining complex values
            # into strings before sending to PyArrow.

            for column in df.columns:

                if df[column].dtype == "object":

                    df[column] = df[column].apply(
                        lambda x:
                        str(x)
                        if isinstance(
                            x,
                            (list, tuple, dict)
                        )
                        else x
                    )

            # ==========================================
            # DISPLAY
            # ==========================================

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # ==========================================
            # DOWNLOAD
            # ==========================================

            csv = df.to_csv(
                index=False
            )

            st.download_button(
                label="⬇ Download CSV",
                data=csv,
                file_name="attpro_scan.csv",
                mime="text/csv"
            )

    else:

        # ==================================================
        # INITIAL KPI CARDS
        # ==================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Stocks Scanned",
                "0"
            )

        with col2:
            st.metric(
                "BUY Signals",
                "0"
            )

        with col3:
            st.metric(
                "HOLD Signals",
                "0"
            )

        with col4:
            st.metric(
                "Average AI Score",
                "0"
            )

        st.info(
            "Select a strategy and click "
            "**🚀 Scan Market** to begin."
        )

    st.divider()

    # ==================================================
    # SYSTEM STATUS
    # ==================================================

    st.subheader("System Status")

    status = pd.DataFrame(
        {
            "Module": [
                "Market Data",
                "Indicators",
                "BTST Strategy",
                "AI Engine",
                "Risk Engine",
                "Ranking Engine",
                "Scanner Engine"
            ],
            "Status": [
                "✅ Online",
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