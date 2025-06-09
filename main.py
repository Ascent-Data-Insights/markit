import polars as pl
from onedrive import read_excel
from search import find_clients


def main():
    print("Hello from markit!")

    df = read_excel()
    existing_clients = pl.Series(df.select("Organization")).to_list()

    new_clients = find_clients(existing_clients=existing_clients)


if __name__ == "__main__":
    main()
