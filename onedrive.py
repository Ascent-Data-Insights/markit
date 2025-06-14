import polars as pl


def read_excel():

    df = pl.read_excel(
        "~/Ascent Data Insights/Initial Planning - Clients/Business Development Prospect List.xlsx"
    )
    return df
