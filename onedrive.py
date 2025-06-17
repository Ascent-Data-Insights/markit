"""Utility functions for interacting with files on local OneDrive."""

import polars as pl


def read_excel():
    """Read the Excel file from local OneDrive and return a Polars DataFrame."""
    df = pl.read_excel("~/Ascent Data Insights/Initial Planning - Clients/Business Development Prospect List.xlsx")
    return df
