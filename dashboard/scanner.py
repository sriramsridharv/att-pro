import streamlit as st
import pandas as pd

from core.scanner_engine import ScannerEngine


def format_conditions(conditions):
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
            formatted.append(f"{condition}: {status}")
        else:
            formatted.append(str(item))

    return " | ".join(formatted)


def format_reasons(reasons):
    if reasons is None:
        return "None"

    if isinstance(reasons, (list, tuple)):
        if len(reasons) == 0:
            return "None"
        return ", ".join(str(reason) for reason in reasons)

    return str(reasons)


def make_streamlit_safe(results):
    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)

    if "Conditions" in df.columns:
        df["Conditions"] = df["Conditions"].apply(format_conditions)

    if "Reasons" in df.columns:
        df["Reasons"] = df["Reasons"].apply(format_reasons)

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].apply(
                lambda x: str(x) if isinstance(x, (list, tuple, dict)) else x
            )

    return df


def show_scanner():
    st.title("🔍 ATT Pro Scanner")
    st.caption("AI-assisted stock scanner powered by technical rules")

    st.sidebar.title("Scanner Options")

    default_symbols = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "BHARTIARTL.NS",
        "AXISBANK.NS",
        "LT.NS",
        "HINDUNILVR.NS",
    ]

    symbols = st.sidebar.multiselect(
        "Symbols to scan",
        default_symbols,
        default=default_symbols[:5],
    )

    custom_symbol = st.sidebar.text_input(
        "Add custom symbol",
        placeholder="TCS.NS",
        key="custom_symbol_input",
    )

    if st.sidebar.button("Add symbol"):
        custom_symbol = custom_symbol.strip().upper()
        if custom_symbol and custom_symbol not in symbols:
            symbols.append(custom_symbol)
            st.sidebar.success(f"Added {custom_symbol}")
        elif not custom_symbol:
            st.sidebar.warning("Enter a valid symbol first.")
        else:
            st.sidebar.info(f"{custom_symbol} is already in the list.")

    strategy = st.sidebar.selectbox(
        "Strategy",
        ["BTST"],
    )

    period = st.sidebar.selectbox(
        "Data period",
        ["1mo", "3mo", "6mo", "1y", "2y"],
        index=2,
    )

    interval = st.sidebar.selectbox(
        "Data interval",
        ["1d", "1h", "15m"],
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.write(
        "Use the scanner to evaluate selected NSE stocks against the BTST strategy."
    )

    scan_clicked = st.sidebar.button("🚀 Scan Market")

    if scan_clicked:
        if not symbols:
            st.warning("Please select one or more symbols before scanning.")
            return

        scanner = ScannerEngine()

        with st.spinner("Scanning market and generating trade signals..."):
            results = scanner.scan_market(symbols, period=period, interval=interval)
            st.session_state["latest_scan_results"] = results

        if not results:
            st.warning("No trading opportunities found or data could not be loaded.")
            return

        df = make_streamlit_safe(results)

        total_stocks = len(df)
        buy_count = int((df["Signal"].astype(str).str.upper() == "BUY").sum()) if "Signal" in df.columns else 0
        hold_count = int((df["Signal"].astype(str).str.upper() == "HOLD").sum()) if "Signal" in df.columns else 0
        average_ai = int(pd.to_numeric(df["AI Score"], errors="coerce").mean()) if "AI Score" in df.columns else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Symbols Scanned", total_stocks)
        col2.metric("BUY Signals", buy_count)
        col3.metric("HOLD Signals", hold_count)
        col4.metric("Avg AI Score", average_ai)

        st.divider()

        if "AI Score" in df.columns:
            df = df.sort_values(by="AI Score", ascending=False)

        st.subheader("Scanner Results")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_data = df.to_csv(index=False)
        st.download_button(
            label="⬇ Download CSV",
            data=csv_data,
            file_name="attpro_scanner_results.csv",
            mime="text/csv",
        )

        st.divider()
        st.subheader("Signal Summaries")

        for item in results:
            symbol = item.get("Symbol", "Unknown")
            signal = item.get("Signal", "N/A")
            score = item.get("Score", "N/A")
            ai_score = item.get("AI Score", "N/A")
            rating = item.get("Rating", "N/A")

            with st.expander(f"{symbol} — {signal} / AI {ai_score}"):
                st.write(f"**Strategy:** {item.get('Strategy', 'BTST')} | **Score:** {score} | **Rating:** {rating}")
                st.write(f"**Entry:** {item.get('Entry')}  |  **Stop Loss:** {item.get('Stop Loss')}")
                st.write(f"**Target 1:** {item.get('Target 1')}  |  **Target 2:** {item.get('Target 2')}")
                st.write(f"**Risk Reward:** {item.get('Risk Reward')}")
                st.write("**Conditions:**")
                st.write(format_conditions(item.get("Conditions")))
                st.write("**Reasons:**")
                st.write(format_reasons(item.get("Reasons")))

    else:
        st.info("Select symbols and click 🚀 Scan Market to evaluate trading signals.")

        st.markdown(
            "#### Quick start\n"
            "1. Choose symbols from the list or add a custom NSE symbol.\n"
            "2. Select the scanning period and interval.\n"
            "3. Click the button to generate signals and trade plan details."
        )
