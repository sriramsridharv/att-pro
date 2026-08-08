import re
import streamlit as st
import pandas as pd
from pathlib import Path

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


def failed_conditions(conditions):
    if not conditions:
        return "None"

    failed = [
        str(condition)
        for condition, passed in conditions
        if not passed
    ]

    return ", ".join(failed) if failed else "None"


def make_streamlit_safe(results):
    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)

    if "Conditions" in df.columns:
        df["Failed Conditions"] = df["Conditions"].apply(failed_conditions)
        df["Conditions"] = df["Conditions"].apply(format_conditions)

    if "Reasons" in df.columns:
        df["Reasons"] = df["Reasons"].apply(format_reasons)

    if "Price" in df.columns and "Price Range" not in df.columns:
        df["Price Range"] = df["Price"].apply(lambda p: price_range_label(float(p)) if pd.notnull(p) else "N/A")

    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].apply(
                lambda x: str(x) if isinstance(x, (list, tuple, dict)) else x
            )

    return df


def load_symbol_file(path="data/symbols.txt"):
    file_path = Path(path)
    if not file_path.exists():
        return []

    symbols = []
    for line in file_path.read_text().splitlines():
        trimmed = line.strip().upper()
        if trimmed and not trimmed.startswith("#"):
            symbols.append(trimmed)

    return symbols


def parse_symbol_list(text):
    if not text:
        return []

    parts = re.split(r"[\n,;]+", text)
    return [item.strip().upper() for item in parts if item.strip()]


def filter_buy_candidates(results):
    """
    Return only results where all BTST conditions passed.
    """
    return [
        item
        for item in results
        if isinstance(item.get("Signal"), str)
        and item.get("Signal").upper() == "BUY"
    ]


def price_range_label(price):
    if price <= 300:
        return "1 - 300"
    if price <= 600:
        return "301 - 600"
    if price <= 900:
        return "601 - 900"
    return "> 900"


def filter_results_by_price_range(results, selected_range):
    if selected_range == "All":
        return results

    def price_in_range(item):
        price = item.get("Price")
        if price is None:
            price = item.get("Entry")
        try:
            price = float(price)
        except (TypeError, ValueError):
            return False

        if selected_range == "1 - 300":
            return price <= 300
        if selected_range == "301 - 600":
            return 300 < price <= 600
        if selected_range == "601 - 900":
            return 600 < price <= 900
        if selected_range == "> 900":
            return price > 900
        return True

    return [item for item in results if price_in_range(item)]


def sort_results(results, sort_key, ascending=True):
    if not results or sort_key is None:
        return results

    def sort_value(item):
        value = item.get(sort_key)
        if sort_key in ["AI Score", "Price"]:
            try:
                return float(value)
            except (TypeError, ValueError):
                return float("-inf") if ascending else float("inf")
        if value is None:
            return ""
        return str(value)

    return sorted(results, key=sort_value, reverse=not ascending)


def show_scanner():
    st.title("🔍 ATT Pro Scanner")
    st.caption("AI-assisted stock scanner powered by technical rules")

    st.sidebar.title("Scanner Options")

    default_symbols = load_symbol_file("data/symbols.txt")

    symbol_groups = {
        "NIFTY50": [
            "ADANIPORTS.NS",
            "ASIANPAINT.NS",
            "AXISBANK.NS",
            "BAJAJ-AUTO.NS",
            "BAJFINANCE.NS",
            "BAJAJFINSV.NS",
            "BPCL.NS",
            "BHARTIARTL.NS",
            "BRITANNIA.NS",
            "CIPLA.NS",
            "COALINDIA.NS",
            "DIVISLAB.NS",
            "DRREDDY.NS",
            "EICHERMOT.NS",
            "GRASIM.NS",
            "HCLTECH.NS",
            "HDFC.NS",
            "HDFCBANK.NS",
            "HDFCLIFE.NS",
            "HEROMOTOCO.NS",
            "HINDALCO.NS",
            "HINDUNILVR.NS",
            "ICICIBANK.NS",
            "ITC.NS",
            "INDUSINDBK.NS",
            "INFY.NS",
            "JSWSTEEL.NS",
            "KOTAKBANK.NS",
            "LT.NS",
            "M&M.NS",
            "MARUTI.NS",
            "NESTLEIND.NS",
            "NTPC.NS",
            "ONGC.NS",
            "POWERGRID.NS",
            "RELIANCE.NS",
            "SBILIFE.NS",
            "SBIN.NS",
            "SUNPHARMA.NS",
            "TCS.NS",
            "TATACHEM.NS",
            "TATACONSUM.NS",
            "TATASTEEL.NS",
            "TECHM.NS",
            "TITAN.NS",
            "ULTRACEMCO.NS",
            "UPL.NS",
            "WIPRO.NS",
            "ZEEL.NS",
        ],
        "Extended Universe": default_symbols,
    }

    if "custom_symbol_groups" not in st.session_state:
        st.session_state["custom_symbol_groups"] = {}

    combined_groups = {**symbol_groups, **st.session_state["custom_symbol_groups"]}

    if "scan_symbols" not in st.session_state:
        st.session_state["scan_symbols"] = combined_groups["NIFTY50"][:10]

    st.sidebar.write(f"Universe loaded: {len(default_symbols)} symbols")

    group_selection = st.sidebar.selectbox(
        "Symbol group",
        list(combined_groups.keys()),
        index=0,
    )

    if st.sidebar.button("Load selected group"):
        st.session_state["scan_symbols"] = combined_groups[group_selection]

    if st.sidebar.button("Select all loaded symbols"):
        st.session_state["scan_symbols"] = combined_groups[group_selection]

    symbols = st.sidebar.multiselect(
        "Symbols to scan",
        default_symbols,
        default=st.session_state["scan_symbols"],
        key="scan_symbols",
    )

    with st.sidebar.expander("Custom symbol groups"):
        custom_group_name = st.text_input(
            "Group name",
            placeholder="My Watchlist",
            key="custom_group_name",
        )
        custom_group_symbols = st.text_area(
            "Symbols (comma/newline separated)",
            placeholder="TCS.NS, RELIANCE.NS, HDFC.NS",
            key="custom_group_symbols",
            height=120,
        )

        if st.button("Save custom group", key="save_custom_group"):
            parsed = parse_symbol_list(custom_group_symbols)
            if not custom_group_name.strip():
                st.sidebar.warning("Enter a valid group name before saving.")
            elif not parsed:
                st.sidebar.warning("Enter at least one symbol for the custom group.")
            else:
                st.session_state["custom_symbol_groups"][custom_group_name.strip()] = parsed
                st.sidebar.success(f"Saved custom group: {custom_group_name.strip()}")

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

    price_range = st.sidebar.selectbox(
        "Price range",
        ["All", "1 - 300", "301 - 600", "601 - 900", "> 900"],
        index=0,
    )

    sort_key = st.sidebar.selectbox(
        "Sort results by",
        ["AI Score", "Price", "Symbol"],
        index=0,
    )

    sort_order = st.sidebar.selectbox(
        "Sort order",
        ["Descending", "Ascending"],
        index=0,
    )

    show_buy_candidates = st.sidebar.checkbox(
        "Show only stocks meeting all conditions",
        value=True,
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

        buy_candidates = filter_buy_candidates(results)
        non_buy_candidates = [item for item in results if item not in buy_candidates]

        if show_buy_candidates:
            results = buy_candidates

        if not results:
            st.warning("No stocks met the selected condition set.")
            return

        results = filter_results_by_price_range(results, price_range)
        results = sort_results(
            results,
            sort_key,
            ascending=(sort_order == "Ascending"),
        )

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

        st.subheader("Buy Candidate List")
        if buy_candidates:
            buy_df = make_streamlit_safe(buy_candidates)
            if "AI Score" in buy_df.columns:
                buy_df = buy_df.sort_values(by="AI Score", ascending=False)
            st.dataframe(buy_df, use_container_width=True, hide_index=True)
        else:
            st.info("No buy candidates found for the selected symbols and timeframe.")

        st.divider()
        st.subheader("Scanner Results")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv_data = df.to_csv(index=False)
        st.download_button(
            label="⬇ Download CSV",
            data=csv_data,
            file_name="attpro_scanner_results.csv",
            mime="text/csv",
        )

        if non_buy_candidates:
            st.divider()
            st.subheader("Failed Conditions Summary")
            failed_summary = []
            for item in non_buy_candidates:
                failed_summary.append(
                    {
                        "Symbol": item.get("Symbol", "Unknown"),
                        "Signal": item.get("Signal", "N/A"),
                        "Failed Conditions": failed_conditions(item.get("Conditions", [])),
                        "Score": item.get("Score", "N/A"),
                    }
                )
            failed_df = pd.DataFrame(failed_summary)
            st.dataframe(failed_df, use_container_width=True, hide_index=True)

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
