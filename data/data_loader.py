"""
data_loader.py
==============

Central data loading manager.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

import pandas as pd

from .base_provider import BaseProvider
from .cache import DataCache


class DataLoader:
    """
    Central manager responsible for loading market data.

    Features
    --------
    - Uses any provider implementing BaseProvider.
    - Optional caching.
    - Unified interface for the rest of the system.
    """

    def __init__(
        self,
        provider: BaseProvider,
        cache: Optional[DataCache] = None,
        use_cache: bool = True,
    ):

        self.provider = provider
        self.cache = cache or DataCache()
        self.use_cache = use_cache

    def load(
        self,
        symbol: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: str = "1d",
    ) -> pd.DataFrame:

        cache_key = self._build_cache_key(
            symbol=symbol,
            start=start,
            end=end,
            interval=interval,
        )

        if self.use_cache and self.cache.exists(cache_key):
            return self.cache.load(cache_key)

        df = self.provider.get_data(
            symbol=symbol,
            start=start,
            end=end,
            interval=interval,
        )

        if self.use_cache:
            self.cache.save(cache_key, df)

        return df

    def _build_cache_key(
        self,
        symbol: str,
        start: Optional[datetime],
        end: Optional[datetime],
        interval: str,
    ) -> str:

        start_str = start.strftime("%Y%m%d") if start else "begin"

        end_str = end.strftime("%Y%m%d") if end else "latest"

        provider_name = (
            self.provider.name()
            .replace(" ", "_")
            .lower()
        )

        return (
            f"{provider_name}_"
            f"{symbol}_"
            f"{interval}_"
            f"{start_str}_"
            f"{end_str}"
        )
