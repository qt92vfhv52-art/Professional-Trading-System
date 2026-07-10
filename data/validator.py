"""
validator.py
============

Validates market data before it enters the trading system.

Author: Mustafa Tariq
Project: Professional Trading System
"""

from __future__ import annotations

import pandas as pd


class DataValidationError(Exception):
    """Raised when market data fails validation."""


class DataValidator:
    """
    Validates OHLCV market data.
    """

    REQUIRED_COLUMNS = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    @classmethod
    def validate(cls, df: pd.DataFrame) -> bool:
        """
        Validate a market DataFrame.

        Parameters
        ----------
        df : pd.DataFrame

        Returns
        -------
        bool

        Raises
        ------
        DataValidationError
        """

        cls._check_dataframe(df)
        cls._check_columns(df)
        cls._check_index(df)
        cls._check_missing_values(df)
        cls._check_duplicate_index(df)
        cls._check_negative_prices(df)
        cls._check_ohlc_logic(df)

        return True

    @staticmethod
    def _check_dataframe(df: pd.DataFrame):

        if not isinstance(df, pd.DataFrame):
            raise DataValidationError(
                "Input must be a pandas DataFrame."
            )

        if df.empty:
            raise DataValidationError(
                "DataFrame is empty."
            )

    @classmethod
    def _check_columns(cls, df):

        missing = [
            col
            for col in cls.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise DataValidationError(
                f"Missing columns: {missing}"
            )

    @staticmethod
    def _check_index(df):

        if not isinstance(df.index, pd.DatetimeIndex):
            raise DataValidationError(
                "Index must be DatetimeIndex."
            )

        if not df.index.is_monotonic_increasing:
            raise DataValidationError(
                "Datetime index must be sorted."
            )

    @staticmethod
    def _check_missing_values(df):

        if df.isnull().values.any():
            raise DataValidationError(
                "Missing values detected."
            )

    @staticmethod
    def _check_duplicate_index(df):

        if df.index.duplicated().any():
            raise DataValidationError(
                "Duplicate timestamps detected."
            )

    @staticmethod
    def _check_negative_prices(df):

        price_columns = [
            "Open",
            "High",
            "Low",
            "Close",
        ]

        if (df[price_columns] <= 0).any().any():
            raise DataValidationError(
                "Price values must be greater than zero."
            )

        if (df["Volume"] < 0).any():
            raise DataValidationError(
                "Volume cannot be negative."
            )

    @staticmethod
    def _check_ohlc_logic(df):

        if (df["High"] < df["Low"]).any():
            raise DataValidationError(
                "High price cannot be lower than Low."
            )

        if (df["Open"] > df["High"]).any():
            raise DataValidationError(
                "Open price exceeds High."
            )

        if (df["Open"] < df["Low"]).any():
            raise DataValidationError(
                "Open price is below Low."
            )

        if (df["Close"] > df["High"]).any():
            raise DataValidationError(
                "Close price exceeds High."
            )

        if (df["Close"] < df["Low"]).any():
            raise DataValidationError(
                "Close price is below Low."
            )
