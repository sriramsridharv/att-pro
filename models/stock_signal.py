from dataclasses import dataclass

@dataclass
class StockSignal:
    symbol: str
    strategy: str
    signal: str
    ai_score: float
    confidence: str
    entry: float
    stop_loss: float
    target: float
    reasons: list[str]
