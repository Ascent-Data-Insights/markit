import polars as pl
from onedrive import read_excel
from search import find_clients, research_client
from anthropic_client import AnthropicClient


def main():
    print("Hello from markit!")

    anthropic_client = AnthropicClient()

    df = read_excel()
    existing_clients = pl.Series(df.select("Organization")).to_list()

    new_clients = find_clients(
        existing_clients=existing_clients, anthropic_client=anthropic_client
    )

    all_research = []
    for client in new_clients.rows(named=True):
        org = client["Organization"]
        research = input(
            f"Would you like to research Organization {org}? (y)/n: "
        ).strip().lower() in ["", "y", "yes"]
        if research:
            research = research_client(
                organization=org, anthropic_client=anthropic_client
            )
            all_research.append(research)
    research_df = pl.concat(all_research, how="vertical")
    research_df = research_df.with_columns(
        [
            pl.col("Technologies Used").list.join("; "),
            pl.col("Technologies Used Citations").list.join("; "),
            pl.col("Trends in Industry").list.join("; "),
            pl.col("Trends in Industry Citations").list.join("; "),
            pl.col("Important Details").list.join("; "),
            pl.col("Important Details Citations").list.join("; "),
        ]
    )
    research_df.write_csv("test.csv")


if __name__ == "__main__":
    main()
