import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def summarize_positions(positions):
    invested = 0.0
    current_value = 0.0
    unrealized = 0.0
    winners = 0
    losers = 0

    for pos in positions:
        invested += float(pos.get("Entry", 0)) * int(pos.get("Quantity", 0))
        current_value += float(pos.get("Current Value", 0))
        unrealized += float(pos.get("Unrealized P/L", 0))
        if pos.get("Unrealized P/L", 0) >= 0:
            winners += 1
        else:
            losers += 1

    return {
        "Invested": invested,
        "Current Value": current_value,
        "Unrealized P/L": unrealized,
        "Winners": winners,
        "Losers": losers,
    }


def make_performance_chart(positions):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[pos["Symbol"] for pos in positions],
            y=[pos["Unrealized P/L"] for pos in positions],
            marker_color=["#2ca02c" if pos["Unrealized P/L"] >= 0 else "#d62728" for pos in positions],
        )
    )
    fig.update_layout(
        title="Position Unrealized P/L",
        xaxis_title="Symbol",
        yaxis_title="P/L (₹)",
        template="plotly_white",
        margin=dict(l=10, r=10, t=35, b=10),
    )
    return fig


def make_allocation_chart(positions):
    labels = [pos["Symbol"] for pos in positions]
    values = [pos["Current Value"] for pos in positions]

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, hole=0.35)]
    )
    fig.update_layout(
        title="Portfolio Allocation by Current Value",
        template="plotly_white",
        margin=dict(l=10, r=10, t=35, b=10),
    )
    return fig


def show_reports():
    st.title("📄 ATT Pro Reports")
    st.caption("Review portfolio performance, scanner activity, and trade insights.")

    positions = st.session_state.get("portfolio_positions", [])
    latest_scan = st.session_state.get("latest_scan_results", [])

    if not positions and not latest_scan:
        st.info("No portfolio or scan data available yet. Add positions or run the scanner first.")
        return

    if positions:
        summary = summarize_positions(positions)

        st.subheader("Portfolio Performance")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Invested", f"₹{summary['Invested']:,.2f}")
        col2.metric("Current Value", f"₹{summary['Current Value']:,.2f}")
        col3.metric("Unrealized P/L", f"₹{summary['Unrealized P/L']:,.2f}")
        col4.metric("Winners", summary["Winners"])
        col5.metric("Losers", summary["Losers"])

        st.divider()
        st.plotly_chart(make_performance_chart(positions), use_container_width=True)
        st.plotly_chart(make_allocation_chart(positions), use_container_width=True)

        st.divider()
        st.subheader("Position Details")
        st.dataframe(pd.DataFrame(positions).round(2), use_container_width=True)

    if latest_scan:
        st.divider()
        st.subheader("Latest Scanner Summary")

        scan_df = pd.DataFrame(latest_scan)
        if "AI Score" in scan_df.columns:
            scan_df = scan_df.sort_values(by="AI Score", ascending=False)

        st.dataframe(scan_df.head(20), use_container_width=True)
        st.markdown(
            "*The scanner summary updates each time you run the market scan on the Scanner page.*"
        )
