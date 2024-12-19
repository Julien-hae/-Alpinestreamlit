"""Main Description."""

import logging

import streamlit as st

from Alpinestreamlit.common.load import load_data
from Alpinestreamlit.common.transform import evaluate_offers

LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the application."""
    LOGGER.info("Executing Streamlit Application.")

    df = load_data("LUXURYESTATE")
    scraped_date = df["DATE"].unique()[0]
    df["SCORE"] = evaluate_offers(df=df)
    df.dropna(inplace=True, subset="PRICE")

    cols_to_display = [
        "SCORE",
        "TITLE",
        "PRICE",
        "URL",
        "ROOMS",
        "BEDROOMS",
        "BATHROOMS",
        "EXTERNAL_SIZE",
        "SIZE",
        "DESCRIPTION",
        "GARDEN",
        "STATUS",
        "ADDRESS",
        "TERRACE",
        "YEAR_OF_CONSTRUCTION",
    ]

    st.title(f"Alpine real estate at {scraped_date}")
    st.dataframe(
        df[cols_to_display], column_config={"URL": st.column_config.LinkColumn()}
    )
    # pressed = st.button("press me")
    # if pressed:
    #     st.title("Hello SBB!")


if __name__ == "__main__":
    main()
