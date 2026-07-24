"""
=========================================================
ATT Pro - Indicator Engine
Author : ATT Pro Team

Calculates technical indicators used by all strategies.
=========================================================
"""

import pandas as pd


class IndicatorEngine:

    def __init__(self):
        pass

    def calculate_indicators(self, df: pd.DataFrame):
        """
        Calculate all technical indicators.
        """

        data = df.copy()

        # ----------------------------
        # Handle MultiIndex columns
        # ----------------------------
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.loc[:, ~data.columns.duplicated()]

        # ----------------------------
        # EMA
        # ----------------------------
        data["EMA20"] = data["Close"].ewm(span=20).mean()
        data["EMA50"] = data["Close"].ewm(span=50).mean()

        # ----------------------------
        # RSI (14)
        # ----------------------------
        delta = data["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        data["RSI"] = 100 - (100 / (1 + rs))

        # ----------------------------
        # Average Volume
        # ----------------------------
        data["AvgVolume20"] = data["Volume"].rolling(20).mean()

        data["VolumeRatio"] = (
            data["Volume"] / data["AvgVolume20"]
        )

        # ----------------------------
        # ATR (14)
        # ----------------------------
        high_low = data["High"] - data["Low"]

        high_close = (
            data["High"] - data["Close"].shift()
        ).abs()

        low_close = (
            data["Low"] - data["Close"].shift()
        ).abs()

        tr = pd.concat(
            [high_low, high_close, low_close],
            axis=1
        ).max(axis=1)

        data["ATR"] = tr.rolling(14).mean()

        return data