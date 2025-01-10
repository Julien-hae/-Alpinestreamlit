"""Contains the multiple transformers for the data."""

import logging
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataframe and add columns."""
    retour_df = df.copy(deep=True)

    retour_df.dropna(subset=["SIZE", "EXTERNAL_SIZE"], how="all", inplace=True)

    retour_df["PRICE_SQ"] = retour_df["PRICE"] / (
        retour_df["SIZE"].fillna(0) + retour_df["EXTERNAL_SIZE"].fillna(0)
    )
    # retour_df['SCORE'] = evaluate_offers(df)
    retour_df.dropna(subset="PRICE_SQ", inplace=True)

    retour_df.dropna(axis=1, how="all", inplace=True)
    retour_df.drop(columns="_id", inplace=True)

    return retour_df


def evaluate_offers(df: pd.DataFrame) -> pd.Series:  # type: ignore
    """Evaluate if real estate offers in a DataFrame are good investments for buying and renting out later.

    :param df: pandas DataFrame, contains the property details with the keys matching the provided column names
    :return: pandas DataFrame, original DataFrame with an added 'Investment_Score' column
    """
    # Define weights for scoring
    weights = {
        "price_sq": -0.4,  # Penalize high prices pro square meter
        "rooms": 0.2,  # More bedrooms = better
        "year_of_construction": 0.1,  # Reward newer properties
    }

    # Helper function to compute individual scores
    def compute_score(row: pd.Series) -> Any:  # type: ignore
        price = row.get("PRICE_SQ", np.nan)
        rooms = row.get("ROOMS", 0)
        year_of_construction = row.get("YEAR_OF_CONSTRUCTION", np.nan)

        # Handle NaN values with defaults
        price = price if not pd.isna(price) else 0
        rooms = rooms if not pd.isna(rooms) else 0
        year_of_construction = (
            year_of_construction if not pd.isna(year_of_construction) else 0
        )

        # Normalize and compute score components
        normalized_price = (
            1 / (price + 1e-6) if price > 0 else 0
        )  # Inverse price (lower price = better score)
        normalized_year = (
            (datetime.today().year - year_of_construction)
            if year_of_construction > 0
            else 0
        )  # Age of property

        score = (
            weights["price_sq"] * normalized_price
            + weights["rooms"] * rooms
            + weights["year_of_construction"] * normalized_year
        )

        return round(score, 2)

    # Ensure missing or unexpected columns do not break processing
    required_columns = [
        "PRICE_SQ",
        "BEDROOMS",
        "BATHROOMS",
        "BALCONY_COUNT",
        "YEAR_OF_CONSTRUCTION",
        "ADDRESS",
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = np.nan
    # Apply the scoring function to each row
    df["SCORE"] = df[required_columns].apply(compute_score, axis=1)
    df["SCORE"] = (df["SCORE"] - df["SCORE"].min()) / (
        df["SCORE"].max() - df["SCORE"].min()
    )

    return df["SCORE"]
