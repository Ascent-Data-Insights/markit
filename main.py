import polars as pl
import typer
from onedrive import read_excel
from search import find_clients, research_client
from anthropic_client import AnthropicClient

app = typer.Typer()


@app.command()
def search_and_research():
    """Find new clients and optionally research them."""
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
    
    if all_research:
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
        print("Research saved to test.csv")


@app.command()
def research(organization: str):
    """Research a specific organization by name."""
    print(f"Researching {organization}...")
    
    anthropic_client = AnthropicClient()
    
    research_df = research_client(
        organization=organization, anthropic_client=anthropic_client
    )
    
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
    
    filename = f"{organization.replace(' ', '_').lower()}_research.csv"
    research_df.write_csv(filename)
    print(f"Research saved to {filename}")


if __name__ == "__main__":
    app()
