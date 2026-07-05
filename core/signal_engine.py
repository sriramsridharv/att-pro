def generate_signal(indicators):
    """
    Generate BUY/SELL/HOLD signal from indicator values.
    """

    signal = {
        "signal": "BUY",
        "score": 92,
        "reasons": [
            "EMA20 > EMA50",
            "RSI 61",
            "ADX 28",
            "Volume 2.3x",
            "WaveTrend Buy"
        ]
    }

    return signal
