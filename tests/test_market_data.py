from data.market_data import MarketData

market = MarketData()

df = market.get_stock_data("RELIANCE.NS")

print(df.tail())
