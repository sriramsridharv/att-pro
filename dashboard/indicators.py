import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit.components.v1 import html

from data.market_data import MarketData
from core.indicator_engine import IndicatorEngine


def make_price_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Close",
            line=dict(color="#1f77b4", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA20"],
            name="EMA20",
            line=dict(color="#ff7f0e", width=2, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA50"],
            name="EMA50",
            line=dict(color="#2ca02c", width=2, dash="dot"),
        )
    )
    fig.update_layout(
        title=f"{symbol} Price with EMA20 / EMA50",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Series",
        template="plotly_white",
        margin=dict(l=10, r=10, t=35, b=10),
    )
    return fig


def make_rsi_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
            name="RSI",
            line=dict(color="#9467bd", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=[70] * len(df),
            name="Overbought",
            line=dict(color="red", width=1, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=[30] * len(df),
            name="Oversold",
            line=dict(color="green", width=1, dash="dash"),
        )
    )
    fig.update_layout(
        title=f"{symbol} RSI (14)",
        xaxis_title="Date",
        yaxis_title="RSI",
        yaxis=dict(range=[0, 100]),
        template="plotly_white",
        legend_title="Series",
        margin=dict(l=10, r=10, t=35, b=10),
    )
    return fig


def make_atr_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["ATR"],
            name="ATR",
            line=dict(color="#8c564b", width=2),
        )
    )
    fig.update_layout(
        title=f"{symbol} ATR (14)",
        xaxis_title="Date",
        yaxis_title="ATR",
        template="plotly_white",
        legend_title="Series",
        margin=dict(l=10, r=10, t=35, b=10),
    )
    return fig


def show_indicators():
    st.title("📊 ATT Pro Indicators")
    st.caption("Visualize technical indicators and price action for NSE stocks.")

    symbols = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "SBIN.NS",
        "BHARTIARTL.NS",
    ]

    st.sidebar.title("Indicators Settings")
    symbol = st.sidebar.selectbox("Select Symbol", symbols, index=0)
    period = st.sidebar.selectbox(
        "Data Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=0
    )
    interval = st.sidebar.selectbox("Data Interval", ["1d", "1h", "15m"], index=0)
    show_volume = st.sidebar.checkbox("Show Volume Chart", value=True)

    st.sidebar.markdown("---")
    st.sidebar.write(
        "Indicators are calculated from price history and shown with latest values. "
        "Use this page to review momentum, trend and volatility for a selected stock."
    )

    if st.sidebar.button("🔄 Load Indicators"):
        market = MarketData()
        indicator_engine = IndicatorEngine()

        with st.spinner("Downloading data and calculating indicators..."):
            df = market.get_stock_data(symbol, period=period, interval=interval)

            if df.empty:
                st.warning("Unable to load data for the selected symbol. Try a different symbol or time interval.")
                return

            df = indicator_engine.calculate_indicators(df)

        latest = df.iloc[-1]
        st.subheader("Latest Indicator Values")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Close", f"{latest['Close']:.2f}")
        col2.metric("EMA20", f"{latest['EMA20']:.2f}")
        col3.metric("EMA50", f"{latest['EMA50']:.2f}")
        col4.metric("RSI", f"{latest['RSI']:.2f}")

        col5, col6, col7 = st.columns(3)
        col5.metric("ATR", f"{latest['ATR']:.2f}")
        col6.metric("Volume Ratio", f"{latest['VolumeRatio']:.2f}")
        col7.metric("Avg Volume (20)", f"{int(latest['AvgVolume20']):,}")

        st.divider()
        st.subheader(f"{symbol} Price and Trend")
        st.plotly_chart(make_price_chart(df, symbol), use_container_width=True)

        st.subheader(f"{symbol} Momentum")
        st.plotly_chart(make_rsi_chart(df, symbol), use_container_width=True)

        st.subheader(f"{symbol} Volatility")
        st.plotly_chart(make_atr_chart(df, symbol), use_container_width=True)

        if show_volume:
            st.subheader(f"{symbol} Volume")
            volume_fig = go.Figure()
            volume_fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["Volume"],
                    name="Volume",
                    marker_color="#17becf",
                )
            )
            volume_fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["AvgVolume20"],
                    name="Avg Volume (20)",
                    line=dict(color="#d62728", width=2),
                )
            )
            volume_fig.update_layout(
                title=f"{symbol} Volume & Average Volume",
                xaxis_title="Date",
                yaxis_title="Volume",
                template="plotly_white",
                legend_title="Series",
                margin=dict(l=10, r=10, t=35, b=10),
            )
            st.plotly_chart(volume_fig, use_container_width=True)

        st.divider()
        st.subheader("TradingView Chart")
        tradingview_symbol = symbol.replace(".NS", ":NSE/")
        tradingview_embed = (
            f"<iframe src=\"https://s.tradingview.com/widgetembed/?frameElementId=tradingview_1&symbol={tradingview_symbol}&interval=60&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=light&style=1&timezone=Etc%2FUTC&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=en\" "
            "width=100% height=610 frameborder=0 allowfullscreen></iframe>"
        )
        html(tradingview_embed, height=620)

        with st.expander("Show raw indicator data"):
            st.dataframe(df.tail(20), use_container_width=True)
    else:
        st.info("Choose a symbol and click 🔄 Load Indicators to render technical charts.")
        st.markdown(
            "#### What this page shows\n"
            "- EMA20 / EMA50 trend and crossover behavior.\n"
            "- RSI momentum and overbought/oversold levels.\n"
            "- ATR volatility and volume context.\n"
        )
