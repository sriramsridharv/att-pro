"""
=========================================================
ATT Pro - Scanner Engine
Author : ATT Pro Team

Scans multiple stocks and returns ranked opportunities.
=========================================================
"""

from data.market_data import MarketData
from core.indicator_engine import IndicatorEngine
from core.ai_engine import AIEngine
from core.ranking_engine import RankingEngine
from core.risk_engine import RiskEngine
from strategies.btst_strategy import BTSTStrategy


class ScannerEngine:

    def __init__(self):

        self.market = MarketData()
        self.indicator = IndicatorEngine()
        self.strategy = BTSTStrategy()
        self.ai = AIEngine()
        self.risk = RiskEngine()
        self.ranking = RankingEngine()

    def scan_market(self, symbols):

        results = []

        for symbol in symbols:

            try:

                # -----------------------------
                # Download Market Data
                # -----------------------------
                df = self.market.get_stock_data(symbol)

                if df.empty:
                    continue

                # -----------------------------
                # Calculate Indicators
                # -----------------------------
                df = self.indicator.calculate_indicators(df)

                # -----------------------------
                # Generate Strategy Signal
                # -----------------------------
                signal = self.strategy.evaluate(df)

                # -----------------------------
                # AI Analysis
                # -----------------------------
                ai_result = self.ai.calculate_ai_score(signal)

                # -----------------------------
                # Risk Management
                # -----------------------------
                trade_plan = self.risk.calculate_trade_plan(df)

                result = {
                    "Symbol": symbol,
                    "Signal": signal["signal"],
                    "Score": int(signal["score"]),
                    "Conditions": signal["conditions"],
                    "AI Score": ai_result["AI Score"],
                    "Rating": ai_result["Rating"],
                    "Reasons": ai_result["Reasons"],
                    "Entry": trade_plan["Entry"],
                    "Stop Loss": trade_plan["Stop Loss"],
                    "Target 1": trade_plan["Target 1"],
                    "Target 2": trade_plan["Target 2"],
                    "Risk Reward": trade_plan["Risk Reward"]
                }

                results.append(result)

            except Exception as e:

                print(f"Error scanning {symbol}")
                print(e)

        # Rank by AI Score
        results = self.ranking.rank(results)

        return results