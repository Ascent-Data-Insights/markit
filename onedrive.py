import polars as pl


def read_excel():

    df = pl.read_excel(
        "~/SharePoint_Initial_Planning/Clients/Business Development Prospect List.xlsx"
    )
    return df
