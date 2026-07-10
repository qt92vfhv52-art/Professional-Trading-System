"""
binance_provider.py
===================

Binance market data provider.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd
from binance.client import Client

from .base_provider import BaseProvider
from .cleaner import DataCleaner
from .validator import DataValidator


class BinanceProvider(BaseProvider):
    """
    Market data provider using Binance API.
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
    ):

        self.client = Client(api_key, api_secret)

    def get_data(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: str = "1d",
    ) -> pd.DataFrame:

        start_str = (
            start.strftime("%d %b %Y %H:%M:%S")
            if start
            else None
        )

        end_str = (
            end.strftime("%d %b %Y %H:%M:%S")
            if end
            else None
        )

        klines = self.client.get_historical_klines(
            symbol,
            interval,
            start_str,
            end_str,
        )

        if not klines:
            raise ValueError(
                f"No data found for symbol '{symbol}'."
            )

        columns = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "CloseTime",
            "QuoteAssetVolume",
            "NumberOfTrades",
            "TakerBuyBaseVolume",
            "TakerBuyQuoteVolume",
            "Ignore",
        ]

        df = pd.DataFrame(klines, columns=columns)

        df = df[
            [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
            ]
        ]

        df["Date"] = pd.to_datetime(
            df["Date"],
            unit="ms",
        )

        df = DataCleaner.clean(df)

        DataValidator.validate(df)

        return df

    def get_available_symbols(self) -> list[str]:

        exchange_info = self.client.get_exchange_info()

        return [
            symbol["symbol"]
            for symbol in exchange_info["symbols"]
        ]

    def name(self) -> str:

        return "Binance"
