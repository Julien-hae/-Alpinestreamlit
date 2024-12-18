"""Main Description."""

import logging

import streamlit as st

LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the application."""
    LOGGER.info("Executing Streamlit Application.")
    pressed = st.button("press me")
    if pressed:
        st.title("Hello SBB!")


if __name__ == "__main__":
    main()
