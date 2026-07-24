from data.market_data import MarketData
from core.indicator_engine import IndicatorEngine
from core.risk_engine import RiskEngine

market = MarketData()
indicator = IndicatorEngine()
risk = RiskEngine()

df = market.get_stock_data("ICICIBANK.NS")
df = indicator.calculate_indicators(df)

plan = risk.calculate_trade_plan(df)

print("\n==============================")
print(" ATT PRO TRADE PLAN")
print("==============================")

for key, value in plan.items():
    print(f"{key:15}: {value}")