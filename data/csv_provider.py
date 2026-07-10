"""
csv_provider.py
===============

CSV market data provider.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Optional

import pandas as pd

from .base_provider import BaseProvider
from .cleaner import DataCleaner
from .validator import DataValidator


class CSVProvider(BaseProvider):
    """
    Load market data from CSV files.
    """

    def __init__(self, file_path: str | Path):

        self.file_path = Path(file_path)

    def get_data(
        self,
        symbol: str = "",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: str = "1d",
    ) -> pd.DataFrame:

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.file_path}"
            )

        df = pd.read_csv(self.file_path)

        df = DataCleaner.clean(df)

        DataValidator.validate(df)

        if start is not None:
            df = df[df.index >= start]

        if end is not None:
            df = df[df.index <= end]

        return df

    def get_available_symbols(self) -> list[str]:

        return [self.file_path.stem]

    def name(self) -> str:

        return "CSV Provider"
