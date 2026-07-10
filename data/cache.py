"""
cache.py
========

Simple file-based cache for market data.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class DataCache:
    """
    Handles caching of market data as parquet files.
    """

    def __init__(self, cache_dir: str | Path = "cache"):

        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def exists(self, key: str) -> bool:

        return self._cache_file(key).exists()

    def load(self, key: str) -> pd.DataFrame:

        return pd.read_parquet(
            self._cache_file(key)
        )

    def save(
        self,
        key: str,
        df: pd.DataFrame,
    ) -> None:

        df.to_parquet(
            self._cache_file(key),
            index=True,
        )

    def delete(self, key: str) -> None:

        file = self._cache_file(key)

        if file.exists():
            file.unlink()

    def clear(self) -> None:

        for file in self.cache_dir.glob("*.parquet"):
            file.unlink()

    def _cache_file(self, key: str) -> Path:

        safe_key = (
            key.replace("/", "_")
               .replace("\\", "_")
               .replace(":", "_")
               .replace(" ", "_")
        )

        return self.cache_dir / f"{safe_key}.parquet"
