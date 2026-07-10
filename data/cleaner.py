"""
cleaner.py
==========

Cleans and standardizes market data before validation.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

import pandas as pd


class DataCleaner:
    """
    Cleans market OHLCV data.

    The cleaner does NOT validate correctness.
    It only standardizes and fixes simple issues.
    """

    COLUMN_MAPPING = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "date": "Date",
        "datetime": "Date",
        "timestamp": "Date",
    }

    @classmethod
    def clean(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a cleaned copy of the DataFrame.
        """

        df = df.copy()

        df = cls._normalize_column_names(df)
        df = cls._set_datetime_index(df)
        df = cls._sort_index(df)
        df = cls._remove_duplicate_rows(df)
        df = cls._convert_numeric(df)

        return df

    @classmethod
    def _normalize_column_names(cls, df: pd.DataFrame) -> pd.DataFrame:

        renamed = {}

        for column in df.columns:

            key = column.strip().lower()

            if key in cls.COLUMN_MAPPING:
                renamed[column] = cls.COLUMN_MAPPING[key]

        return df.rename(columns=renamed)

    @staticmethod
    def _set_datetime_index(df: pd.DataFrame) -> pd.DataFrame:

        if isinstance(df.index, pd.DatetimeIndex):
            return df

        if "Date" in df.columns:

            df["Date"] = pd.to_datetime(df["Date"])

            df = df.set_index("Date")

        return df

    @staticmethod
    def _sort_index(df: pd.DataFrame) -> pd.DataFrame:

        return df.sort_index()

    @staticmethod
    def _remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:

        df = df[~df.index.duplicated(keep="first")]

        return df

    @staticmethod
    def _convert_numeric(df: pd.DataFrame) -> pd.DataFrame:

        columns = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        for column in columns:

            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce",
                )

        return df
