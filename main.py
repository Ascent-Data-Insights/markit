"""Main script for searching and researching clients using AI interfaces."""

import datetime as dt

import polars as pl
import typer

from ai_interfaces.anthropic_interface import AnthropicInterface
from ai_interfaces.base_interface import BaseInterface
from ai_interfaces.perplexity_interface import PerplexityInterface
from onedrive import read_excel
from search import find_clients, research_client

app = typer.Typer()


def interface_constructor(name: str) -> BaseInterface:
    """Construct an AI client based on the provided name."""
    if name.lower() == "anthropic":
        return AnthropicInterface()
    elif name.lower() == "perplexity":
        return PerplexityInterface()
    else:
        raise ValueError(f"Unknown client name: {name}")


@app.command()
def search_and_research(ai_interface: str = "perplexity"):
    """Find new clients and optionally research them."""
    print("Hello from markit!")

    ai_interface = interface_constructor(ai_interface)

    df = read_excel()
    existing_clients = pl.Series(df.select("Organization")).to_list()

    new_clients = find_clients(existing_clients=existing_clients, ai_interface=ai_interface)

    all_research = []
    for client in new_clients.rows(named=True):
        org = client["Organization"]
        research = input(f"Would you like to research Organization {org}? (y)/n: ").strip().lower() in ["", "y", "yes"]
        if research:
            research = research_client(organization=org, ai_interface=ai_interface)
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
        filename = f"research_results_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        research_df.write_csv(filename)
        print(f"Research saved to {filename}")


@app.command()
def research(organization: str, ai_interface: str = "perplexity"):
    """Research a specific organization by name."""
    print(f"Researching {organization}...")

    ai_interface = interface_constructor(ai_interface)

    research_df = research_client(organization=organization, ai_interface=ai_interface)

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
