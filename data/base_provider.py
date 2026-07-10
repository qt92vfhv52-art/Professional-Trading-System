"""
base_provider.py
================

Abstract interface for all market data providers.

Every provider (Yahoo, Binance, CSV, Polygon, etc.)
must inherit from BaseProvider and implement the
required methods.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import pandas as pd


class BaseProvider(ABC):
    """
    Abstract base class for all market data providers.

    Every provider must return a pandas DataFrame
    with the following columns:

    - Open
    - High
    - Low
    - Close
    - Volume

    Index:
        DatetimeIndex
    """

    @abstractmethod
    def get_data(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Download or load historical market data.

        Parameters
        ----------
        symbol : str
            Trading symbol.
            Example:
                BTCUSDT
                AAPL
                EURUSD

        start : datetime | None
            Start date.

        end : datetime | None
            End date.

        interval : str
            Candle timeframe.

        Returns
        -------
        pd.DataFrame
            OHLCV DataFrame.
        """
        raise NotImplementedError

    @abstractmethod
    def get_available_symbols(self) -> list[str]:
        """
        Return all supported symbols.

        Returns
        -------
        list[str]
        """
        raise NotImplementedError

    @abstractmethod
    def name(self) -> str:
        """
        Provider name.

        Example
        -------
        Yahoo Finance
        Binance
        CSV

        Returns
        -------
        str
        """
        raise NotImplementedError
