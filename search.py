"""Functions for finding and researching potential clients for Ascent Data Insights."""

import json

import polars as pl

from ai_interfaces.base_interface import BaseInterface


def parse_json(
    message: str,
) -> tuple[pl.DataFrame, bool]:
    """Attempt to parse JSON from a string.

    Just tries to shove the provided message into JSON. If it fails, we return
    False, signaling for a retry.
    """
    try:
        valid_json = json.loads(message)
        df = pl.DataFrame(valid_json)
        return df, True
    except json.JSONDecodeError:
        return pl.DataFrame(), False


def find_clients(existing_clients: list[str], ai_interface: BaseInterface) -> pl.DataFrame:
    """Find clients for Ascent!.

    The purpose of this function is a first, high level search of names of potential clients.
    We do not ask for much detail here, just who they are, some basic links, and why the AI
    thinks they might be a good choice.

    Args:
    ----
        existing_clients: A list of strings containing the names of organizations already in our
            contact list. We will instruct the AI to avoid these.
        ai_interface: The AI client to use for research.

    Returns:
    -------
        A Polars DataFrame with client information.

    """
    prompt = f"""
        Begin by searching the web for companies in Cincinati, Dayton, and Northern Kentucky
        that would be great clients for Ascent Data Insights.
        Provide me with your top 5 choices.

        Below is a list of existing clients we have contacted already, do not include anyone from this list
        in your recommendations.
        {existing_clients}

        Focus on companies that are small to medium sized businesses, such as HVAC, Home Services, Restaurants, etc.
        Companies like tech startups should be ignored. Healthcare is okay, but should be deprioritized.

        Return your result as valid JSON List with an entry per company in the following format:
        "Organization" (string), "Industry" (string), "Links" (list[string]), "Reason" (string)

        ONLY return the JSON and no other text. You can include your reason for choosing this company in the "Reason" section of the JSON.
        There should be no text before the JSON, and no text after the JSON. Every field must contain information, links are not
        allowed to be empty or null. Provide links for every company.
    """

    success = False
    attempts = 1
    df = None
    while not success and attempts <= 5:

        print(f"Client search attempt {attempts} ...")
        message = ai_interface.create_message(prompt=prompt)
        print("Raw message:", message)

        df, success = parse_json(message=message)
        attempts += 1

    if df is None:
        raise ValueError("Failed to generate valid JSON")

    print("New Leads Generated!")
    print(df)
    return df


def research_client(organization: pl.Series, ai_interface: BaseInterface) -> pl.DataFrame:
    """Provide deeper, in depth research on a particular potential client.

    Args:
    ----
        organization: A series of info on the company we want to do business on. Should
            be a row from find_clients().
        ai_interface: The AI client to use for research.

    Returns:
    -------
        A Polars DataFrame with added information about the lead.

    """
    prompt = f"""
        Please do some web search research on the business **{organization}** in the Greater Cincinnati
        area. We would like to answer the following questions:

        * Who should we contact to try to pitch this company? Typically this will be an owner or CTO.
        * What is their name, work email, and/or work phone number?
        * If they have a generic email or phone nuber for the business, get that as well.
        * Estimated Revenue
        * Estimated Employee Count
        * Any mentions of technologies they use, like databases, SaaS companies, cloud providers, etc.
        * Do broader research on this industry and help us understand the big trends in this industry right now.
        * Call out three important details about this company.

        Return your result as valid JSON List with an entry per company in the following format:
        "Organization" (string), Contact Name (string), Contact Role (string), Contact Phone Number (string),
        Contact Email (string), Contact Citation [string], Generic Email (string), Generic Phone Number (string), Generic Citation [string],
        Revenue (number), Headcount (number),
        Technologies Used (List[string]), Technologies Used Citations [list[string]], Trends in Industry (List[string]),
        Trends in Industry Citations [list[string][, Important Details (List[string]), Important Details Citations [list[string]].

        ONLY return the JSON and no other text. There should be no text before the JSON, and no text after the JSON.
        Each of the "Citations" Fields should contain a valid URL to where you got this particular information. Double check
        that all provided links are valid and go to live web pages referencing where you got that particular information.
    """

    success = False
    attempts = 1
    df = None
    while not success and attempts <= 5:

        print(f"Client research attempt {attempts} ...")
        message = ai_interface.create_message(prompt=prompt)

        df, success = parse_json(message=message)
        attempts += 1

    if df is None:
        raise ValueError("Failed to generate valid JSON")

    # Handle empty (not found) values
    # If a value is empty, we want to replace it with a list of an empty string
    # TODO: a more elegant way to do this?
    df = df.with_columns(
        [
            pl.when(pl.col("Technologies Used").is_null() | pl.col("Technologies Used").list.len() == 0)
            .then([""])
            .otherwise(pl.col("Technologies Used"))
            .alias("Technologies Used"),
            pl.when(pl.col("Technologies Used Citations").is_null() | pl.col("Technologies Used Citations").list.len() == 0)
            .then([""])
            .otherwise(pl.col("Technologies Used Citations"))
            .alias("Technologies Used Citations"),
            pl.when(pl.col("Trends in Industry").is_null() | pl.col("Trends in Industry").list.len() == 0)
            .then([""])
            .otherwise(pl.col("Trends in Industry"))
            .alias("Trends in Industry"),
            pl.when(pl.col("Trends in Industry Citations").is_null() | pl.col("Trends in Industry Citations").list.len() == 0)
            .then([""])
            .otherwise(pl.col("Trends in Industry Citations"))
            .alias("Trends in Industry Citations"),
            pl.when(pl.col("Important Details").is_null() | pl.col("Important Details").list.len() == 0)
            .then([""])
            .otherwise(pl.col("Important Details"))
            .alias("Important Details"),
            pl.when(pl.col("Important Details Citations").is_null() | pl.col("Important Details Citations").list.len() == 0)
            .then([""])
            .otherwise(pl.col("Important Details Citations"))
            .alias("Important Details Citations"),
        ]
    )

    print("Research Generated!")
    print(df)
    return df
