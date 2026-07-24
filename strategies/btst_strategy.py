"""
=========================================================
ATT Pro - BTST Strategy
Author : ATT Pro Team

Buy Today Sell Tomorrow Strategy
=========================================================
"""

BTST_RULES = {
    "ema20_above_ema50": True,
    "close_above_ema20": True,
    "rsi_min": 55,
    "volume_multiplier": 1.5,
}


class BTSTStrategy:

    def __init__(self):
        self.rules = BTST_RULES

    def evaluate(self, data):
        """
        Evaluate BTST conditions using the latest candle.
        """

        latest = data.iloc[-1]

        conditions = [
            (
                "EMA20 > EMA50",
                latest["EMA20"] > latest["EMA50"]
            ),
            (
                "Close > EMA20",
                latest["Close"] > latest["EMA20"]
            ),
            (
                "RSI > 55",
                latest["RSI"] > self.rules["rsi_min"]
            ),
            (
                "Volume > 1.5x Avg",
                latest["VolumeRatio"] > self.rules["volume_multiplier"]
            )
        ]

        score = sum(1 for _, passed in conditions if passed)

        signal = "BUY" if score >= 4 else "HOLD"

        return {
            "strategy": "BTST",
            "signal": signal,
            "score": score,
            "conditions": conditions
        }