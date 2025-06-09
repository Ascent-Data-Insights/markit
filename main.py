import polars as pl
from onedrive import read_excel
from search import find_clients
from anthropic_client import AnthropicClient


def main():
    print("Hello from markit!")

    anthropic_client = AnthropicClient()
    
    df = read_excel()
    existing_clients = pl.Series(df.select("Organization")).to_list()

    new_clients = find_clients(existing_clients=existing_clients, anthropic_client=anthropic_client)


if __name__ == "__main__":
    main()
