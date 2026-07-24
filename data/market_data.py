"""
=========================================================
ATT Pro - Market Data Engine
Author : ATT Pro Team

Description:
Downloads historical stock market data using Yahoo Finance.
=========================================================
"""

import yfinance as yf
import pandas as pd


class MarketData:

    def __init__(self):
        pass

    def get_stock_data(
        self,
        symbol,
        period="6mo",
        interval="1d"
    ):
        """
        Download OHLCV data for a single stock.

        Parameters
        ----------
        symbol : str
            NSE symbol (Example: RELIANCE.NS)

        period : str
            1mo, 3mo, 6mo, 1y, 2y, 5y, max

        interval : str
            1d, 1h, 15m, 5m

        Returns
        -------
        pandas.DataFrame
        """

        try:

            data = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True
            )

            # ---------------------------------------
            # Handle MultiIndex columns (newer yfinance)
            # ---------------------------------------
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            # Remove duplicate columns
            data = data.loc[:, ~data.columns.duplicated()]

            # Keep only required columns
            required_columns = [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]

            data = data[required_columns]

            if data.empty:
                print(f"No data found for {symbol}")
                return pd.DataFrame()

            data.dropna(inplace=True)

            return data

        except Exception as e:

            print(f"Error downloading {symbol}")
            print(e)

            return pd.DataFrame()

    def get_multiple_stocks(
        self,
        symbols,
        period="6mo",
        interval="1d"
    ):
        """
        Download multiple stocks.

        Returns
        -------
        Dictionary
        {
            "RELIANCE.NS": dataframe,
            "SBIN.NS": dataframe
        }
        """

        market = {}

        for symbol in symbols:

            market[symbol] = self.get_stock_data(
                symbol,
                period,
                interval
            )

        return market