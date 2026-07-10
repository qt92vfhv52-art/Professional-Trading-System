"""
yahoo_provider.py
=================

Yahoo Finance data provider.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd
import yfinance as yf

from .base_provider import BaseProvider
from .cleaner import DataCleaner
from .validator import DataValidator


class YahooProvider(BaseProvider):
    """
    Market data provider using Yahoo Finance.
    """

    def get_data(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: str = "1d",
    ) -> pd.DataFrame:

        df = yf.download(
            tickers=symbol,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )

        if df.empty:
            raise ValueError(
                f"No data found for symbol '{symbol}'."
            )

        df = DataCleaner.clean(df)

        DataValidator.validate(df)

        return df

    def get_available_symbols(self) -> list[str]:
        """
        Yahoo Finance supports thousands of symbols.
        Listing all of them is not practical.
        """

        raise NotImplementedError(
            "Yahoo Finance does not provide a complete symbol list."
        )

    def name(self) -> str:

        return "Yahoo Finance"
