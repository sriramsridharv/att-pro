import streamlit as st


def initialize_settings():
    if "attpro_settings" not in st.session_state:
        st.session_state["attpro_settings"] = {
            "symbols": [
                "RELIANCE.NS",
                "TCS.NS",
                "INFY.NS",
                "HDFCBANK.NS",
                "ICICIBANK.NS",
                "SBIN.NS",
            ],
            "default_period": "6mo",
            "default_interval": "1d",
            "risk_pct": 1.5,
            "reward_ratio": 2.0,
        }


def show_settings():
    st.title("⚙️ ATT Pro Settings")
    st.caption("Configure scanner defaults, risk parameters, and favored symbols.")

    initialize_settings()
    settings = st.session_state["attpro_settings"]

    with st.form("settings_form"):
        st.subheader("Scanner Defaults")
        settings["symbols"] = st.text_area(
            "Default Symbols (one per line)",
            value="\n".join(settings["symbols"]),
            height=150,
        ).strip().upper().splitlines()

        settings["default_period"] = st.selectbox(
            "Default Data Period",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=["1mo", "3mo", "6mo", "1y", "2y"].index(settings["default_period"]),
        )

        settings["default_interval"] = st.selectbox(
            "Default Data Interval",
            ["1d", "1h", "15m"],
            index=["1d", "1h", "15m"].index(settings["default_interval"]),
        )

        st.subheader("Risk Management")
        settings["risk_pct"] = st.number_input(
            "Default Risk % per trade",
            min_value=0.1,
            max_value=10.0,
            value=settings["risk_pct"],
            step=0.1,
            format="%.1f",
        )

        settings["reward_ratio"] = st.number_input(
            "Default Reward Ratio",
            min_value=1.0,
            max_value=5.0,
            value=settings["reward_ratio"],
            step=0.1,
            format="%.1f",
        )

        submitted = st.form_submit_button("Save Settings")

        if submitted:
            st.success("Settings updated successfully.")

    st.divider()
    st.subheader("Current Settings")
    st.write(settings)

    if st.button("Reset to default settings"):
        st.session_state["attpro_settings"] = {
            "symbols": [
                "RELIANCE.NS",
                "TCS.NS",
                "INFY.NS",
                "HDFCBANK.NS",
                "ICICIBANK.NS",
                "SBIN.NS",
            ],
            "default_period": "6mo",
            "default_interval": "1d",
            "risk_pct": 1.5,
            "reward_ratio": 2.0,
        }
        st.success("Settings reset to defaults.")
