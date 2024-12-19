"""Contains the multiple transformers for the data."""

from typing import Any

import numpy as np
import pandas as pd


def evaluate_offers(df: pd.DataFrame) -> pd.Series:  # type: ignore
    """Evaluate if real estate offers in a DataFrame are good investments for buying and renting out later.

    :param df: pandas DataFrame, contains the property details with the keys matching the provided column names
    :return: pandas DataFrame, original DataFrame with an added 'Investment_Score' column
    """
    # Define weights for scoring
    weights = {
        "price": -0.4,  # Penalize high prices
        "size": 0.3,  # Reward larger size
        "bedrooms": 0.2,  # More bedrooms = better
        "bathrooms": 0.1,  # More bathrooms = better
        "balcony": 0.1,  # Reward balcony availability
        "year_of_construction": 0.1,  # Reward newer properties
        "missing_values_penalty": -0.05,  # Penalize rows with missing values
    }

    # Helper function to compute individual scores
    def compute_score(row: pd.Series) -> Any:  # type: ignore
        price = row.get("PRICE", np.nan)
        size = row.get("SIZE", np.nan)
        bedrooms = row.get("BEDROOMS", 0)
        bathrooms = row.get("BATHROOMS", 0)
        balcony = row.get("BALCONY_COUNT", 0)
        year_of_construction = row.get("YEAR_OF_CONSTRUCTION", np.nan)
        location = row.get("ADDRESS", "")

        # Handle NaN values with defaults
        price = price if not pd.isna(price) else 0
        size = size if not pd.isna(size) else 0
        bedrooms = bedrooms if not pd.isna(bedrooms) else 0
        bathrooms = bathrooms if not pd.isna(bathrooms) else 0
        balcony = balcony if not pd.isna(balcony) else 0
        location = location if not pd.isna(location) else ""
        year_of_construction = (
            year_of_construction if not pd.isna(year_of_construction) else 0
        )

        # Count missing values in the row
        missing_values_count = row.isna().sum()

        # Normalize and compute score components
        normalized_price = (
            1 / (price + 1e-6) if price > 0 else 0
        )  # Inverse price (lower price = better score)
        normalized_size = size  # Direct size contribution
        normalized_year = (
            (2024 - year_of_construction) if year_of_construction > 0 else 0
        )  # Age of property

        score = (
            weights["price"] * normalized_price
            + weights["size"] * normalized_size
            + weights["bedrooms"] * bedrooms
            + weights["bathrooms"] * bathrooms
            + weights["balcony"] * balcony
            + weights["year_of_construction"] * normalized_year
            + weights["missing_values_penalty"]
            * missing_values_count  # Penalize for missing values
        )

        # Adjust score for location desirability (placeholder for actual location scoring model)
        if "luxury" in location.lower():
            score += 0.2  # Bonus for luxury locations

        return round(score, 2)

    # Ensure missing or unexpected columns do not break processing
    required_columns = [
        "PRICE",
        "SIZE",
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

    return df["SCORE"]
