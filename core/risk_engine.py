"""
=========================================================
ATT Pro - Risk Management Engine
Author : ATT Pro Team

Calculates Entry, Stop Loss, Targets,
Risk and Reward based on ATR.
=========================================================
"""


class RiskEngine:

    def __init__(self):
        pass

    def calculate_trade_plan(self, data):

        """
        Calculate trade plan using latest candle.
        """

        latest = data.iloc[-1]

        entry = round(float(latest["Close"]), 2)
        atr = round(float(latest["ATR"]), 2)

        stop_loss = round(entry - (1.5 * atr), 2)

        target1 = round(entry + (2 * atr), 2)

        target2 = round(entry + (4 * atr), 2)

        risk = round(entry - stop_loss, 2)

        reward = round(target1 - entry, 2)

        rr_ratio = round(reward / risk, 2) if risk > 0 else 0

        return {
            "Entry": entry,
            "ATR": atr,
            "Stop Loss": stop_loss,
            "Target 1": target1,
            "Target 2": target2,
            "Risk": risk,
            "Reward": reward,
            "Risk Reward": rr_ratio
        }