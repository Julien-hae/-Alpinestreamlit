"""Main Description."""

import logging

import pandas as pd
import plotly.express as px
import streamlit as st

from Alpinestreamlit.common.load import load_data
from Alpinestreamlit.common.transform import clean_dataframe

LOGGER = logging.getLogger(__name__)


def create_histogram(df, x, title, nbins=100, color="#636EFA"):
    """Create a Plotly histogram."""
    hist = px.histogram(
        df,
        x=x,
        title=title,
        nbins=nbins,
        color_discrete_sequence=[color],
        marginal="box",
        opacity=0.75,
    )
    hist.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        xaxis_title=x,
        yaxis_title="Nombre d'observations",
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        bargap=0.2,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    return hist


def create_bar(
    df, x, y, orientation="h", title="Bar Plot", color=None, color_scale="Blues"
):
    """Create a Plotly bar plot."""
    bar = px.bar(
        df,
        x=x,
        y=y,
        orientation=orientation,
        title=title,
        color=color,
        color_continuous_scale=color_scale,
    )
    bar.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        xaxis_title=x,
        yaxis_title=y,
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    bar.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    return bar


def create_line(df, x, y, color, title):
    """Create a Plotly line plot."""
    line = px.line(df, x=x, y=y, color=color, title=title)
    line.update_layout(
        title={"text": title, "x": 0.5, "xanchor": "center"},
        xaxis_title=x,
        yaxis_title=y,
        font=dict(family="Arial, sans-serif", size=12, color="Black"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    line.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    line.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGray")
    return line


def main() -> None:
    """Main entry point for the application."""
    LOGGER.info("Executing Streamlit Application.")

    # Load data
    df = load_data()
    df = clean_dataframe(df)

    # Process data
    scraped_date = df["DATE"].max()
    unique_df = df[df["DATE"] == scraped_date].drop_duplicates(subset="REFERENCE")
    nan_df = (
        pd.DataFrame({"column": df.columns, "nan_perc": df.isna().mean() * 100})
        .reset_index(drop=True)
        .sort_values(by="nan_perc", ascending=True)
    )

    # Number of objects scraped per "AGENCY" over time
    agency_counts = df.groupby(["DATE", "AGENCY"]).size().reset_index(name="count")

    # Create plots
    price_hist = create_histogram(
        unique_df, x="PRICE_SQ", title="Distribution du prix au mètre carré"
    )
    nan_fig = create_bar(
        nan_df,
        x="nan_perc",
        y="column",
        title="NaN Percentage per Column",
        color="nan_perc",
    )
    agency_fig = create_line(
        agency_counts,
        x="DATE",
        y="count",
        color="AGENCY",
        title="Number of Objects Scraped per Agency Over Time",
    )

    agency_count_bar = unique_df["AGENCY"].value_counts().reset_index()
    agency_count_bar.columns = ["AGENCY", "count"]
    agency_count_bar = agency_count_bar.sort_values(by="count", ascending=True)
    agency_bar_fig = create_bar(
        agency_count_bar,
        x="count",
        y="AGENCY",
        orientation="h",
        title="Number of Objects Scraped per Agency",
        color="count",
        color_scale="Viridis",
    )

    price_dist_fig = create_histogram(
        unique_df, x="PRICE", title="Distribution of Prices", color="#EF553B"
    )

    # Create streamlit
    st.set_page_config(
        page_title="Alpine Real Estate Dashboard",
        page_icon="🏡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title(f"Alpine real estate at {scraped_date}")
    cola1, cola2, cola3 = st.columns(3)
    colb1, colb2, colb3 = st.columns(3)

    with cola1:
        st.plotly_chart(agency_bar_fig)
    with cola2:
        st.plotly_chart(agency_fig)
    with cola3:
        st.plotly_chart(nan_fig)
    with colb1:
        st.plotly_chart(price_hist)
    with colb2:
        st.dataframe(unique_df, column_config={"URL": st.column_config.LinkColumn()})
    with colb3:
        st.plotly_chart(price_dist_fig)


if __name__ == "__main__":
    main()
