from core.scanner_engine import ScannerEngine

scanner = ScannerEngine()

stocks = [
    "ICICIBANK.NS",
    "SBIN.NS",
    "INFY.NS",
    "TCS.NS",
    "RELIANCE.NS"
]

results = scanner.scan_market(stocks)

print("\n========================================")
print("        ATT PRO MARKET SCANNER")
print("========================================")

for stock in results:

    print(f"\nStock        : {stock['Symbol']}")
    print(f"Signal       : {stock['Signal']}")
    print(f"AI Score     : {stock['AI Score']}")
    print(f"Rating       : {stock['Rating']}")
    print(f"Entry        : {stock['Entry']}")
    print(f"Stop Loss    : {stock['Stop Loss']}")
    print(f"Target 1     : {stock['Target 1']}")
    print(f"Target 2     : {stock['Target 2']}")
    print(f"Risk Reward  : {stock['Risk Reward']}")