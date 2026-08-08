import streamlit as st
import pandas as pd

from data.market_data import MarketData


def initialize_portfolio_state():
    if "portfolio_positions" not in st.session_state:
        st.session_state["portfolio_positions"] = []

    if "portfolio_settings" not in st.session_state:
        st.session_state["portfolio_settings"] = {
            "starting_capital": 100000.0,
            "default_risk_pct": 1.5,
            "default_reward_ratio": 2.0,
        }


def calculate_position_metrics(position, latest_price):
    entry = float(position["Entry"])
    quantity = int(position["Quantity"])
    direction = position["Direction"]

    notional = entry * quantity
    current_value = latest_price * quantity

    if direction == "Long":
        pnl = (latest_price - entry) * quantity
        return_pct = pnl / notional * 100 if notional else 0
    else:
        pnl = (entry - latest_price) * quantity
        return_pct = pnl / notional * 100 if notional else 0

    return {
        "Current Price": latest_price,
        "Current Value": round(current_value, 2),
        "Unrealized P/L": round(pnl, 2),
        "Return %": round(return_pct, 2),
    }


def show_portfolio():
    st.title("💼 ATT Pro Portfolio")
    st.caption("Monitor positions, risk and portfolio performance.")

    initialize_portfolio_state()

    settings = st.session_state["portfolio_settings"]

    with st.sidebar.expander("Portfolio Settings", expanded=True):
        settings["starting_capital"] = st.number_input(
            "Starting Capital",
            min_value=1000.0,
            value=settings["starting_capital"],
            step=1000.0,
            format="%.2f",
        )
        settings["default_risk_pct"] = st.number_input(
            "Default Risk %",
            min_value=0.1,
            max_value=10.0,
            value=settings["default_risk_pct"],
            step=0.1,
            format="%.1f",
        )
        settings["default_reward_ratio"] = st.number_input(
            "Default Reward Ratio",
            min_value=1.0,
            max_value=5.0,
            value=settings["default_reward_ratio"],
            step=0.1,
            format="%.1f",
        )

    with st.form("add_position_form"):
        st.subheader("Add New Position")
        col1, col2, col3 = st.columns(3)

        symbol = col1.text_input("Symbol", value="RELIANCE.NS")
        direction = col2.selectbox("Direction", ["Long", "Short"])
        quantity = col3.number_input(
            "Quantity",
            min_value=1,
            value=10,
            step=1,
        )

        col4, col5, col6 = st.columns(3)
        entry = col4.number_input(
            "Entry Price",
            min_value=0.01,
            value=1000.0,
            step=1.0,
            format="%.2f",
        )
        stop_loss = col5.number_input(
            "Stop Loss",
            min_value=0.01,
            value=950.0,
            step=1.0,
            format="%.2f",
        )
        target = col6.number_input(
            "Target Price",
            min_value=0.01,
            value=1100.0,
            step=1.0,
            format="%.2f",
        )

        notes = st.text_area("Notes", value="")
        add_position = st.form_submit_button("Add Position")

        if add_position:
            position = {
                "Symbol": symbol.strip().upper(),
                "Direction": direction,
                "Quantity": quantity,
                "Entry": entry,
                "Stop Loss": stop_loss,
                "Target": target,
                "Notes": notes,
            }
            st.session_state["portfolio_positions"].append(position)
            st.success(f"Added position for {symbol.strip().upper()}")

    positions = st.session_state["portfolio_positions"]

    st.divider()
    st.subheader("Portfolio Summary")

    if not positions:
        st.info("Add a position to start tracking your portfolio.")
        return

    market = MarketData()
    enriched = []
    total_invested = 0.0
    total_value = 0.0
    total_unrealized = 0.0

    for position in positions:
        symbol = position["Symbol"]
        df = market.get_stock_data(symbol, period="1mo", interval="1d")
        latest_price = float(df["Close"].iloc[-1]) if not df.empty else float(position["Entry"])

        metrics = calculate_position_metrics(position, latest_price)
        enriched_position = {**position, **metrics}

        total_invested += float(position["Entry"]) * int(position["Quantity"])
        total_value += metrics["Current Value"]
        total_unrealized += metrics["Unrealized P/L"]
        enriched.append(enriched_position)

    df_positions = pd.DataFrame(enriched)
    df_positions = df_positions.round(2)

    total_positions = len(enriched)
    average_return = round((total_unrealized / total_invested) * 100, 2) if total_invested else 0.0

    st.metric("Open Positions", total_positions)
    st.metric("Total Invested", f"₹{total_invested:,.2f}")
    st.metric("Current Value", f"₹{total_value:,.2f}")
    st.metric("Unrealized P/L", f"₹{total_unrealized:,.2f}")
    st.metric("Portfolio Return", f"{average_return:.2f}%")

    st.divider()
    st.dataframe(df_positions, use_container_width=True)

    if st.button("Clear All Positions"):
        st.session_state["portfolio_positions"] = []
        st.success("Portfolio positions cleared.")
