from data.market_data import MarketData
from core.indicator_engine import IndicatorEngine

market = MarketData()

indicator = IndicatorEngine()

df = market.get_stock_data("RELIANCE.NS")

df = indicator.calculate_indicators(df)

print(df.tail())
